/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#include <algorithm>

#include <yoga/Yoga.h>

#include "./Config.h"
#include "./Bounds.h"
#include "./LayoutNode.h"
#include "./Size.h"

static YGSize globalMeasureFunc(
    YGNodeConstRef nodeRef,
    float width,
    YGMeasureMode widthMode,
    float height,
    YGMeasureMode heightMode)
{
  LayoutNode const &node = *reinterpret_cast<LayoutNode const *>(YGNodeGetContext(nodeRef));

  Size size = node.callMeasureFunc(width, widthMode, height, heightMode);
  YGSize ygSize = {
      static_cast<float>(size.width), static_cast<float>(size.height)};

  return ygSize;
}

static void globalDirtiedFunc(YGNodeConstRef nodeRef)
{
  LayoutNode const &node = *reinterpret_cast<LayoutNode const *>(YGNodeGetContext(nodeRef));

  node.callDirtiedFunc();
}

/* static */ LayoutNode *LayoutNode::createDefault(void)
{
  return new LayoutNode(nullptr);
}

/* static */ LayoutNode *LayoutNode::createWithConfig(Config *config)
{
  return new LayoutNode(config);
}

/* static */ void LayoutNode::destroy(LayoutNode *node)
{
  delete node;
}

/* static */ LayoutNode *LayoutNode::fromYGNode(YGNodeRef nodeRef)
{
  return reinterpret_cast<LayoutNode *>(YGNodeGetContext(nodeRef));
}

LayoutNode::LayoutNode(Config *config)
    : m_node(
          config != nullptr ? YGNodeNewWithConfig(config->m_config)
                            : YGNodeNew())
{
  YGNodeSetContext(m_node, reinterpret_cast<void *>(this));
}

LayoutNode::~LayoutNode(void)
{
  YGNodeFree(m_node);
}

void LayoutNode::reset(void)
{
  m_measureFunc = py::none();
  m_dirtiedFunc = py::none();

  YGNodeReset(m_node);
}

void LayoutNode::copyStyle(LayoutNode const &other)
{
  YGNodeCopyStyle(m_node, other.m_node);
}

void LayoutNode::setBoxSizing(int boxSizing)
{
  YGNodeStyleSetBoxSizing(m_node, static_cast<YGBoxSizing>(boxSizing));
}

void LayoutNode::setPositionType(int positionType)
{
  YGNodeStyleSetPositionType(m_node, static_cast<YGPositionType>(positionType));
}

void LayoutNode::setPosition(int edge, double position)
{
  YGNodeStyleSetPosition(m_node, static_cast<YGEdge>(edge), position);
}

void LayoutNode::setPositionPercent(int edge, double position)
{
  YGNodeStyleSetPositionPercent(m_node, static_cast<YGEdge>(edge), position);
}

void LayoutNode::setPositionAuto(int edge)
{
  YGNodeStyleSetPositionAuto(m_node, static_cast<YGEdge>(edge));
}

void LayoutNode::setAlignContent(facebook::yoga::Align alignContent)
{
  YGNodeStyleSetAlignContent(m_node, static_cast<YGAlign>(alignContent));
}

void LayoutNode::setAlignItems(int alignItems)
{
  YGNodeStyleSetAlignItems(m_node, static_cast<YGAlign>(alignItems));
}

void LayoutNode::setAlignSelf(int alignSelf)
{
  YGNodeStyleSetAlignSelf(m_node, static_cast<YGAlign>(alignSelf));
}

void LayoutNode::setFlexDirection(int flexDirection)
{
  YGNodeStyleSetFlexDirection(
      m_node, static_cast<YGFlexDirection>(flexDirection));
}

void LayoutNode::setDirection(int direction)
{
  YGNodeStyleSetDirection(m_node, static_cast<YGDirection>(direction));
}

void LayoutNode::setFlexWrap(int flexWrap)
{
  YGNodeStyleSetFlexWrap(m_node, static_cast<YGWrap>(flexWrap));
}

void LayoutNode::setJustifyContent(int justifyContent)
{
  YGNodeStyleSetJustifyContent(m_node, static_cast<YGJustify>(justifyContent));
}

void LayoutNode::setMargin(int edge, double margin)
{
  YGNodeStyleSetMargin(m_node, static_cast<YGEdge>(edge), margin);
}

void LayoutNode::setMarginPercent(int edge, double margin)
{
  YGNodeStyleSetMarginPercent(m_node, static_cast<YGEdge>(edge), margin);
}

void LayoutNode::setMarginAuto(int edge)
{
  YGNodeStyleSetMarginAuto(m_node, static_cast<YGEdge>(edge));
}

void LayoutNode::setOverflow(int overflow)
{
  YGNodeStyleSetOverflow(m_node, static_cast<YGOverflow>(overflow));
}

void LayoutNode::setDisplay(int display)
{
  YGNodeStyleSetDisplay(m_node, static_cast<YGDisplay>(display));
}

void LayoutNode::setFlex(double flex)
{
  YGNodeStyleSetFlex(m_node, flex);
}

void LayoutNode::setFlexBasis(double flexBasis)
{
  YGNodeStyleSetFlexBasis(m_node, flexBasis);
}

void LayoutNode::setFlexBasisPercent(double flexBasis)
{
  YGNodeStyleSetFlexBasisPercent(m_node, flexBasis);
}

void LayoutNode::setFlexBasisAuto()
{
  YGNodeStyleSetFlexBasisAuto(m_node);
}

void LayoutNode::setFlexBasisMaxContent()
{
  YGNodeStyleSetFlexBasisMaxContent(m_node);
}

void LayoutNode::setFlexBasisFitContent()
{
  YGNodeStyleSetFlexBasisFitContent(m_node);
}

void LayoutNode::setFlexBasisStretch()
{
  YGNodeStyleSetFlexBasisStretch(m_node);
}

void LayoutNode::setFlexGrow(double flexGrow)
{
  YGNodeStyleSetFlexGrow(m_node, flexGrow);
}

void LayoutNode::setFlexShrink(double flexShrink)
{
  YGNodeStyleSetFlexShrink(m_node, flexShrink);
}

void LayoutNode::setWidth(double width)
{
  YGNodeStyleSetWidth(m_node, width);
}

void LayoutNode::setWidthPercent(double width)
{
  YGNodeStyleSetWidthPercent(m_node, width);
}

void LayoutNode::setWidthAuto()
{
  YGNodeStyleSetWidthAuto(m_node);
}

void LayoutNode::setWidthMaxContent()
{
  YGNodeStyleSetWidthMaxContent(m_node);
}

void LayoutNode::setWidthFitContent()
{
  YGNodeStyleSetWidthFitContent(m_node);
}

void LayoutNode::setWidthStretch()
{
  YGNodeStyleSetWidthStretch(m_node);
}

void LayoutNode::setHeight(double height)
{
  YGNodeStyleSetHeight(m_node, height);
}

void LayoutNode::setHeightPercent(double height)
{
  YGNodeStyleSetHeightPercent(m_node, height);
}

void LayoutNode::setHeightAuto()
{
  YGNodeStyleSetHeightAuto(m_node);
}

void LayoutNode::setHeightMaxContent()
{
  YGNodeStyleSetHeightMaxContent(m_node);
}

void LayoutNode::setHeightFitContent()
{
  YGNodeStyleSetHeightFitContent(m_node);
}

void LayoutNode::setHeightStretch()
{
  YGNodeStyleSetHeightStretch(m_node);
}

void LayoutNode::setMinWidth(double minWidth)
{
  YGNodeStyleSetMinWidth(m_node, minWidth);
}

void LayoutNode::setMinWidthPercent(double minWidth)
{
  YGNodeStyleSetMinWidthPercent(m_node, minWidth);
}

void LayoutNode::setMinWidthMaxContent()
{
  YGNodeStyleSetMinWidthMaxContent(m_node);
}

void LayoutNode::setMinWidthFitContent()
{
  YGNodeStyleSetMinWidthFitContent(m_node);
}

void LayoutNode::setMinWidthStretch()
{
  YGNodeStyleSetMinWidthStretch(m_node);
}

void LayoutNode::setMinHeight(double minHeight)
{
  YGNodeStyleSetMinHeight(m_node, minHeight);
}

void LayoutNode::setMinHeightPercent(double minHeight)
{
  YGNodeStyleSetMinHeightPercent(m_node, minHeight);
}

void LayoutNode::setMinHeightMaxContent()
{
  YGNodeStyleSetMinHeightMaxContent(m_node);
}

void LayoutNode::setMinHeightFitContent()
{
  YGNodeStyleSetMinHeightFitContent(m_node);
}

void LayoutNode::setMinHeightStretch()
{
  YGNodeStyleSetMinHeightStretch(m_node);
}

void LayoutNode::setMaxWidth(double maxWidth)
{
  YGNodeStyleSetMaxWidth(m_node, maxWidth);
}

void LayoutNode::setMaxWidthPercent(double maxWidth)
{
  YGNodeStyleSetMaxWidthPercent(m_node, maxWidth);
}

void LayoutNode::setMaxWidthMaxContent()
{
  YGNodeStyleSetMaxWidthMaxContent(m_node);
}

void LayoutNode::setMaxWidthFitContent()
{
  YGNodeStyleSetMaxWidthFitContent(m_node);
}

void LayoutNode::setMaxWidthStretch()
{
  YGNodeStyleSetMaxWidthStretch(m_node);
}

void LayoutNode::setMaxHeight(double maxHeight)
{
  YGNodeStyleSetMaxHeight(m_node, maxHeight);
}

void LayoutNode::setMaxHeightPercent(double maxHeight)
{
  YGNodeStyleSetMaxHeightPercent(m_node, maxHeight);
}

void LayoutNode::setMaxHeightMaxContent()
{
  YGNodeStyleSetMaxHeightMaxContent(m_node);
}

void LayoutNode::setMaxHeightFitContent()
{
  YGNodeStyleSetMaxHeightFitContent(m_node);
}

void LayoutNode::setMaxHeightStretch()
{
  YGNodeStyleSetMaxHeightStretch(m_node);
}

void LayoutNode::setAspectRatio(double aspectRatio)
{
  YGNodeStyleSetAspectRatio(m_node, aspectRatio);
}

void LayoutNode::setBorder(int edge, double border)
{
  YGNodeStyleSetBorder(m_node, static_cast<YGEdge>(edge), border);
}

void LayoutNode::setPadding(int edge, double padding)
{
  YGNodeStyleSetPadding(m_node, static_cast<YGEdge>(edge), padding);
}

void LayoutNode::setPaddingPercent(int edge, double padding)
{
  YGNodeStyleSetPaddingPercent(m_node, static_cast<YGEdge>(edge), padding);
}

void LayoutNode::setIsReferenceBaseline(bool isReferenceBaseline)
{
  YGNodeSetIsReferenceBaseline(m_node, isReferenceBaseline);
}

void LayoutNode::setGap(int gutter, double gapLength)
{
  YGNodeStyleSetGap(m_node, static_cast<YGGutter>(gutter), gapLength);
}

void LayoutNode::setGapPercent(int gutter, double gapLength)
{
  YGNodeStyleSetGapPercent(m_node, static_cast<YGGutter>(gutter), gapLength);
}

int LayoutNode::getBoxSizing(void) const
{
  return YGNodeStyleGetBoxSizing(m_node);
}

int LayoutNode::getPositionType(void) const
{
  return YGNodeStyleGetPositionType(m_node);
}

Value LayoutNode::getPosition(int edge) const
{
  return Value::fromYGValue(
      YGNodeStyleGetPosition(m_node, static_cast<YGEdge>(edge)));
}

int LayoutNode::getAlignContent(void) const
{
  return YGNodeStyleGetAlignContent(m_node);
}

int LayoutNode::getAlignItems(void) const
{
  return YGNodeStyleGetAlignItems(m_node);
}

int LayoutNode::getAlignSelf(void) const
{
  return YGNodeStyleGetAlignSelf(m_node);
}

int LayoutNode::getFlexDirection(void) const
{
  return YGNodeStyleGetFlexDirection(m_node);
}

int LayoutNode::getDirection(void) const
{
  return YGNodeStyleGetDirection(m_node);
}

int LayoutNode::getFlexWrap(void) const
{
  return YGNodeStyleGetFlexWrap(m_node);
}

int LayoutNode::getJustifyContent(void) const
{
  return YGNodeStyleGetJustifyContent(m_node);
}

Value LayoutNode::getMargin(int edge) const
{
  return Value::fromYGValue(
      YGNodeStyleGetMargin(m_node, static_cast<YGEdge>(edge)));
}

int LayoutNode::getOverflow(void) const
{
  return YGNodeStyleGetOverflow(m_node);
}

int LayoutNode::getDisplay(void) const
{
  return YGNodeStyleGetDisplay(m_node);
}

Value LayoutNode::getFlexBasis(void) const
{
  return Value::fromYGValue(YGNodeStyleGetFlexBasis(m_node));
}

double LayoutNode::getFlexGrow(void) const
{
  return YGNodeStyleGetFlexGrow(m_node);
}

double LayoutNode::getFlexShrink(void) const
{
  return YGNodeStyleGetFlexShrink(m_node);
}

Value LayoutNode::getWidth(void) const
{
  return Value::fromYGValue(YGNodeStyleGetWidth(m_node));
}

Value LayoutNode::getHeight(void) const
{
  return Value::fromYGValue(YGNodeStyleGetHeight(m_node));
}

Value LayoutNode::getMinWidth(void) const
{
  return Value::fromYGValue(YGNodeStyleGetMinWidth(m_node));
}

Value LayoutNode::getMinHeight(void) const
{
  return Value::fromYGValue(YGNodeStyleGetMinHeight(m_node));
}

Value LayoutNode::getMaxWidth(void) const
{
  return Value::fromYGValue(YGNodeStyleGetMaxWidth(m_node));
}

Value LayoutNode::getMaxHeight(void) const
{
  return Value::fromYGValue(YGNodeStyleGetMaxHeight(m_node));
}

double LayoutNode::getAspectRatio(void) const
{
  return YGNodeStyleGetAspectRatio(m_node);
}

double LayoutNode::getBorder(int edge) const
{
  return YGNodeStyleGetBorder(m_node, static_cast<YGEdge>(edge));
}

Value LayoutNode::getPadding(int edge) const
{
  return Value::fromYGValue(
      YGNodeStyleGetPadding(m_node, static_cast<YGEdge>(edge)));
}

Value LayoutNode::getGap(int gutter) const
{
  return Value::fromYGValue(
      YGNodeStyleGetGap(m_node, static_cast<YGGutter>(gutter)));
}

bool LayoutNode::isReferenceBaseline()
{
  return YGNodeIsReferenceBaseline(m_node);
}

void LayoutNode::insertChild(py::object py_child, unsigned index)
{
  // Extract C++ pointer from the Python object
  LayoutNode *child = py_child.cast<LayoutNode *>();
  YGNodeInsertChild(m_node, child->m_node, index);
  py_children.insert(py_children.begin() + index, py_child);
}
/*
void Node::insertChild(Node* child, unsigned index) {
  YGNodeInsertChild(m_node, child->m_node, index);
}
*/
void LayoutNode::addChild(py::object py_child)
{
  // Extract C++ pointer from the Python object
  LayoutNode *child = py_child.cast<LayoutNode *>();
  YGNodeInsertChild(m_node, child->m_node, YGNodeGetChildCount(m_node));
  py_children.push_back(py_child);
}

void LayoutNode::removeChild(LayoutNode *child)
{
  YGNodeRemoveChild(m_node, child->m_node);
}

unsigned LayoutNode::getChildCount(void) const
{
  return YGNodeGetChildCount(m_node);
}

LayoutNode *LayoutNode::getParent(void)
{
  auto nodePtr = YGNodeGetParent(m_node);

  if (nodePtr == nullptr)
    return nullptr;

  return LayoutNode::fromYGNode(nodePtr);
}

LayoutNode *LayoutNode::getChild(unsigned index)
{
  auto nodePtr = YGNodeGetChild(m_node, index);

  if (nodePtr == nullptr)
    return nullptr;

  return LayoutNode::fromYGNode(nodePtr);
}

void LayoutNode::setMeasureFunc(py::function measureFunc)
{
  m_measureFunc = measureFunc;

  YGNodeSetMeasureFunc(m_node, &globalMeasureFunc);
}

void LayoutNode::unsetMeasureFunc(void)
{
  // m_measureFunc.reset(nullptr);
  m_measureFunc = py::none();

  YGNodeSetMeasureFunc(m_node, nullptr);
}

Size LayoutNode::callMeasureFunc(
    double width,
    int widthMode,
    double height,
    int heightMode) const
{
  // return m_measureFunc->measure(width, widthMode, height, heightMode);
  if (!m_measureFunc)
  {
    throw std::runtime_error("Measure function is not set.");
  }
  py::gil_scoped_acquire acquire;
  py::object result = m_measureFunc(width, widthMode, height, heightMode);
  if (!py::isinstance<Size>(result))
  {
    throw std::runtime_error("Measure function must return a Size object.");
  }
  Size size = result.cast<Size>();
  if (size.width < 0 || size.height < 0)
  {
    throw std::runtime_error("Measure function returned negative dimensions.");
  }
  return size;
  // return py::cast<Size>(m_measureFunc(width, widthMode, height, heightMode));
}

void LayoutNode::setDirtiedFunc(py::function dirtiedFunc)
{
  // m_dirtiedFunc.reset(dirtiedFunc);
  m_dirtiedFunc = dirtiedFunc;

  YGNodeSetDirtiedFunc(m_node, &globalDirtiedFunc);
}

void LayoutNode::unsetDirtiedFunc(void)
{
  // m_dirtiedFunc.reset(nullptr);
  m_dirtiedFunc = py::none();

  YGNodeSetDirtiedFunc(m_node, nullptr);
}

void LayoutNode::callDirtiedFunc(void) const
{
  // m_dirtiedFunc->dirtied();
  if (!m_dirtiedFunc)
  {
    throw std::runtime_error("Dirtied function is not set.");
  }
  py::gil_scoped_acquire acquire;
  m_dirtiedFunc();
}

void LayoutNode::markDirty(void)
{
  YGNodeMarkDirty(m_node);
}

bool LayoutNode::isDirty(void) const
{
  return YGNodeIsDirty(m_node);
}

void LayoutNode::markLayoutSeen()
{
  YGNodeSetHasNewLayout(m_node, false);
}

bool LayoutNode::hasNewLayout(void) const
{
  return YGNodeGetHasNewLayout(m_node);
}

// void Node::calculateLayout(double width, double height, int direction) {
void LayoutNode::calculateBounds(double width, double height, facebook::yoga::Direction direction)
{
  YGNodeCalculateLayout(
      m_node, width, height, static_cast<YGDirection>(direction));
}

double LayoutNode::getComputedLeft(void) const
{
  return YGNodeLayoutGetLeft(m_node);
}

double LayoutNode::getComputedRight(void) const
{
  return YGNodeLayoutGetRight(m_node);
}

double LayoutNode::getComputedTop(void) const
{
  return YGNodeLayoutGetTop(m_node);
}

double LayoutNode::getComputedBottom(void) const
{
  return YGNodeLayoutGetBottom(m_node);
}

double LayoutNode::getComputedWidth(void) const
{
  return YGNodeLayoutGetWidth(m_node);
}

double LayoutNode::getComputedHeight(void) const
{
  return YGNodeLayoutGetHeight(m_node);
}

Bounds LayoutNode::getComputedBounds(void) const
{
  Bounds layout;

  layout.left = YGNodeLayoutGetLeft(m_node);
  layout.right = YGNodeLayoutGetRight(m_node);

  layout.top = YGNodeLayoutGetTop(m_node);
  layout.bottom = YGNodeLayoutGetBottom(m_node);

  layout.width = YGNodeLayoutGetWidth(m_node);
  layout.height = YGNodeLayoutGetHeight(m_node);

  return layout;
}

double LayoutNode::getComputedMargin(int edge) const
{
  return YGNodeLayoutGetMargin(m_node, static_cast<YGEdge>(edge));
}

double LayoutNode::getComputedBorder(int edge) const
{
  return YGNodeLayoutGetBorder(m_node, static_cast<YGEdge>(edge));
}

double LayoutNode::getComputedPadding(int edge) const
{
  return YGNodeLayoutGetPadding(m_node, static_cast<YGEdge>(edge));
}

void LayoutNode::setAlwaysFormsContainingBlock(bool alwaysFormsContainingBlock)
{
  return YGNodeSetAlwaysFormsContainingBlock(
      m_node, alwaysFormsContainingBlock);
}
