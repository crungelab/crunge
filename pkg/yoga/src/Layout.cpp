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
#include "./Layout.h"
#include "./Size.h"

static YGSize globalMeasureFunc(
    YGNodeConstRef nodeRef,
    float width,
    YGMeasureMode widthMode,
    float height,
    YGMeasureMode heightMode) {
  Layout const& node = *reinterpret_cast<Layout const*>(YGNodeGetContext(nodeRef));

  Size size = node.callMeasureFunc(width, widthMode, height, heightMode);
  YGSize ygSize = {
      static_cast<float>(size.width), static_cast<float>(size.height)};

  return ygSize;
}

static void globalDirtiedFunc(YGNodeConstRef nodeRef) {
  Layout const& node = *reinterpret_cast<Layout const*>(YGNodeGetContext(nodeRef));

  node.callDirtiedFunc();
}

/* static */ Layout* Layout::createDefault(void) {
  return new Layout(nullptr);
}

/* static */ Layout* Layout::createWithConfig(Config* config) {
  return new Layout(config);
}

/* static */ void Layout::destroy(Layout* node) {
  delete node;
}

/* static */ Layout* Layout::fromYGNode(YGNodeRef nodeRef) {
  return reinterpret_cast<Layout*>(YGNodeGetContext(nodeRef));
}

Layout::Layout(Config* config)
    : m_node(
          config != nullptr ? YGNodeNewWithConfig(config->m_config)
                            : YGNodeNew()),
      m_measureFunc(nullptr),
      m_dirtiedFunc(nullptr) {
  YGNodeSetContext(m_node, reinterpret_cast<void*>(this));
}

Layout::~Layout(void) {
  YGNodeFree(m_node);
}

void Layout::reset(void) {
  m_measureFunc.reset(nullptr);
  m_dirtiedFunc.reset(nullptr);

  YGNodeReset(m_node);
}

void Layout::copyStyle(Layout const& other) {
  YGNodeCopyStyle(m_node, other.m_node);
}

void Layout::setBoxSizing(int boxSizing) {
  YGNodeStyleSetBoxSizing(m_node, static_cast<YGBoxSizing>(boxSizing));
}

void Layout::setPositionType(int positionType) {
  YGNodeStyleSetPositionType(m_node, static_cast<YGPositionType>(positionType));
}

void Layout::setPosition(int edge, double position) {
  YGNodeStyleSetPosition(m_node, static_cast<YGEdge>(edge), position);
}

void Layout::setPositionPercent(int edge, double position) {
  YGNodeStyleSetPositionPercent(m_node, static_cast<YGEdge>(edge), position);
}

void Layout::setPositionAuto(int edge) {
  YGNodeStyleSetPositionAuto(m_node, static_cast<YGEdge>(edge));
}

void Layout::setAlignContent(facebook::yoga::Align alignContent) {
  YGNodeStyleSetAlignContent(m_node, static_cast<YGAlign>(alignContent));
}

void Layout::setAlignItems(int alignItems) {
  YGNodeStyleSetAlignItems(m_node, static_cast<YGAlign>(alignItems));
}

void Layout::setAlignSelf(int alignSelf) {
  YGNodeStyleSetAlignSelf(m_node, static_cast<YGAlign>(alignSelf));
}

void Layout::setFlexDirection(int flexDirection) {
  YGNodeStyleSetFlexDirection(
      m_node, static_cast<YGFlexDirection>(flexDirection));
}

void Layout::setDirection(int direction) {
  YGNodeStyleSetDirection(m_node, static_cast<YGDirection>(direction));
}

void Layout::setFlexWrap(int flexWrap) {
  YGNodeStyleSetFlexWrap(m_node, static_cast<YGWrap>(flexWrap));
}

void Layout::setJustifyContent(int justifyContent) {
  YGNodeStyleSetJustifyContent(m_node, static_cast<YGJustify>(justifyContent));
}

void Layout::setMargin(int edge, double margin) {
  YGNodeStyleSetMargin(m_node, static_cast<YGEdge>(edge), margin);
}

void Layout::setMarginPercent(int edge, double margin) {
  YGNodeStyleSetMarginPercent(m_node, static_cast<YGEdge>(edge), margin);
}

void Layout::setMarginAuto(int edge) {
  YGNodeStyleSetMarginAuto(m_node, static_cast<YGEdge>(edge));
}

void Layout::setOverflow(int overflow) {
  YGNodeStyleSetOverflow(m_node, static_cast<YGOverflow>(overflow));
}

void Layout::setDisplay(int display) {
  YGNodeStyleSetDisplay(m_node, static_cast<YGDisplay>(display));
}

void Layout::setFlex(double flex) {
  YGNodeStyleSetFlex(m_node, flex);
}

void Layout::setFlexBasis(double flexBasis) {
  YGNodeStyleSetFlexBasis(m_node, flexBasis);
}

void Layout::setFlexBasisPercent(double flexBasis) {
  YGNodeStyleSetFlexBasisPercent(m_node, flexBasis);
}

void Layout::setFlexBasisAuto() {
  YGNodeStyleSetFlexBasisAuto(m_node);
}

void Layout::setFlexBasisMaxContent() {
  YGNodeStyleSetFlexBasisMaxContent(m_node);
}

void Layout::setFlexBasisFitContent() {
  YGNodeStyleSetFlexBasisFitContent(m_node);
}

void Layout::setFlexBasisStretch() {
  YGNodeStyleSetFlexBasisStretch(m_node);
}

void Layout::setFlexGrow(double flexGrow) {
  YGNodeStyleSetFlexGrow(m_node, flexGrow);
}

void Layout::setFlexShrink(double flexShrink) {
  YGNodeStyleSetFlexShrink(m_node, flexShrink);
}

void Layout::setWidth(double width) {
  YGNodeStyleSetWidth(m_node, width);
}

void Layout::setWidthPercent(double width) {
  YGNodeStyleSetWidthPercent(m_node, width);
}

void Layout::setWidthAuto() {
  YGNodeStyleSetWidthAuto(m_node);
}

void Layout::setWidthMaxContent() {
  YGNodeStyleSetWidthMaxContent(m_node);
}

void Layout::setWidthFitContent() {
  YGNodeStyleSetWidthFitContent(m_node);
}

void Layout::setWidthStretch() {
  YGNodeStyleSetWidthStretch(m_node);
}

void Layout::setHeight(double height) {
  YGNodeStyleSetHeight(m_node, height);
}

void Layout::setHeightPercent(double height) {
  YGNodeStyleSetHeightPercent(m_node, height);
}

void Layout::setHeightAuto() {
  YGNodeStyleSetHeightAuto(m_node);
}

void Layout::setHeightMaxContent() {
  YGNodeStyleSetHeightMaxContent(m_node);
}

void Layout::setHeightFitContent() {
  YGNodeStyleSetHeightFitContent(m_node);
}

void Layout::setHeightStretch() {
  YGNodeStyleSetHeightStretch(m_node);
}

void Layout::setMinWidth(double minWidth) {
  YGNodeStyleSetMinWidth(m_node, minWidth);
}

void Layout::setMinWidthPercent(double minWidth) {
  YGNodeStyleSetMinWidthPercent(m_node, minWidth);
}

void Layout::setMinWidthMaxContent() {
  YGNodeStyleSetMinWidthMaxContent(m_node);
}

void Layout::setMinWidthFitContent() {
  YGNodeStyleSetMinWidthFitContent(m_node);
}

void Layout::setMinWidthStretch() {
  YGNodeStyleSetMinWidthStretch(m_node);
}

void Layout::setMinHeight(double minHeight) {
  YGNodeStyleSetMinHeight(m_node, minHeight);
}

void Layout::setMinHeightPercent(double minHeight) {
  YGNodeStyleSetMinHeightPercent(m_node, minHeight);
}

void Layout::setMinHeightMaxContent() {
  YGNodeStyleSetMinHeightMaxContent(m_node);
}

void Layout::setMinHeightFitContent() {
  YGNodeStyleSetMinHeightFitContent(m_node);
}

void Layout::setMinHeightStretch() {
  YGNodeStyleSetMinHeightStretch(m_node);
}

void Layout::setMaxWidth(double maxWidth) {
  YGNodeStyleSetMaxWidth(m_node, maxWidth);
}

void Layout::setMaxWidthPercent(double maxWidth) {
  YGNodeStyleSetMaxWidthPercent(m_node, maxWidth);
}

void Layout::setMaxWidthMaxContent() {
  YGNodeStyleSetMaxWidthMaxContent(m_node);
}

void Layout::setMaxWidthFitContent() {
  YGNodeStyleSetMaxWidthFitContent(m_node);
}

void Layout::setMaxWidthStretch() {
  YGNodeStyleSetMaxWidthStretch(m_node);
}

void Layout::setMaxHeight(double maxHeight) {
  YGNodeStyleSetMaxHeight(m_node, maxHeight);
}

void Layout::setMaxHeightPercent(double maxHeight) {
  YGNodeStyleSetMaxHeightPercent(m_node, maxHeight);
}

void Layout::setMaxHeightMaxContent() {
  YGNodeStyleSetMaxHeightMaxContent(m_node);
}

void Layout::setMaxHeightFitContent() {
  YGNodeStyleSetMaxHeightFitContent(m_node);
}

void Layout::setMaxHeightStretch() {
  YGNodeStyleSetMaxHeightStretch(m_node);
}

void Layout::setAspectRatio(double aspectRatio) {
  YGNodeStyleSetAspectRatio(m_node, aspectRatio);
}

void Layout::setBorder(int edge, double border) {
  YGNodeStyleSetBorder(m_node, static_cast<YGEdge>(edge), border);
}

void Layout::setPadding(int edge, double padding) {
  YGNodeStyleSetPadding(m_node, static_cast<YGEdge>(edge), padding);
}

void Layout::setPaddingPercent(int edge, double padding) {
  YGNodeStyleSetPaddingPercent(m_node, static_cast<YGEdge>(edge), padding);
}

void Layout::setIsReferenceBaseline(bool isReferenceBaseline) {
  YGNodeSetIsReferenceBaseline(m_node, isReferenceBaseline);
}

void Layout::setGap(int gutter, double gapLength) {
  YGNodeStyleSetGap(m_node, static_cast<YGGutter>(gutter), gapLength);
}

void Layout::setGapPercent(int gutter, double gapLength) {
  YGNodeStyleSetGapPercent(m_node, static_cast<YGGutter>(gutter), gapLength);
}

int Layout::getBoxSizing(void) const {
  return YGNodeStyleGetBoxSizing(m_node);
}

int Layout::getPositionType(void) const {
  return YGNodeStyleGetPositionType(m_node);
}

Value Layout::getPosition(int edge) const {
  return Value::fromYGValue(
      YGNodeStyleGetPosition(m_node, static_cast<YGEdge>(edge)));
}

int Layout::getAlignContent(void) const {
  return YGNodeStyleGetAlignContent(m_node);
}

int Layout::getAlignItems(void) const {
  return YGNodeStyleGetAlignItems(m_node);
}

int Layout::getAlignSelf(void) const {
  return YGNodeStyleGetAlignSelf(m_node);
}

int Layout::getFlexDirection(void) const {
  return YGNodeStyleGetFlexDirection(m_node);
}

int Layout::getDirection(void) const {
  return YGNodeStyleGetDirection(m_node);
}

int Layout::getFlexWrap(void) const {
  return YGNodeStyleGetFlexWrap(m_node);
}

int Layout::getJustifyContent(void) const {
  return YGNodeStyleGetJustifyContent(m_node);
}

Value Layout::getMargin(int edge) const {
  return Value::fromYGValue(
      YGNodeStyleGetMargin(m_node, static_cast<YGEdge>(edge)));
}

int Layout::getOverflow(void) const {
  return YGNodeStyleGetOverflow(m_node);
}

int Layout::getDisplay(void) const {
  return YGNodeStyleGetDisplay(m_node);
}

Value Layout::getFlexBasis(void) const {
  return Value::fromYGValue(YGNodeStyleGetFlexBasis(m_node));
}

double Layout::getFlexGrow(void) const {
  return YGNodeStyleGetFlexGrow(m_node);
}

double Layout::getFlexShrink(void) const {
  return YGNodeStyleGetFlexShrink(m_node);
}

Value Layout::getWidth(void) const {
  return Value::fromYGValue(YGNodeStyleGetWidth(m_node));
}

Value Layout::getHeight(void) const {
  return Value::fromYGValue(YGNodeStyleGetHeight(m_node));
}

Value Layout::getMinWidth(void) const {
  return Value::fromYGValue(YGNodeStyleGetMinWidth(m_node));
}

Value Layout::getMinHeight(void) const {
  return Value::fromYGValue(YGNodeStyleGetMinHeight(m_node));
}

Value Layout::getMaxWidth(void) const {
  return Value::fromYGValue(YGNodeStyleGetMaxWidth(m_node));
}

Value Layout::getMaxHeight(void) const {
  return Value::fromYGValue(YGNodeStyleGetMaxHeight(m_node));
}

double Layout::getAspectRatio(void) const {
  return YGNodeStyleGetAspectRatio(m_node);
}

double Layout::getBorder(int edge) const {
  return YGNodeStyleGetBorder(m_node, static_cast<YGEdge>(edge));
}

Value Layout::getPadding(int edge) const {
  return Value::fromYGValue(
      YGNodeStyleGetPadding(m_node, static_cast<YGEdge>(edge)));
}

Value Layout::getGap(int gutter) const {
  return Value::fromYGValue(
      YGNodeStyleGetGap(m_node, static_cast<YGGutter>(gutter)));
}

bool Layout::isReferenceBaseline() {
  return YGNodeIsReferenceBaseline(m_node);
}

void Layout::insertChild(py::object py_child, unsigned index) {
    // Extract C++ pointer from the Python object
    Layout* child = py_child.cast<Layout*>();
    YGNodeInsertChild(m_node, child->m_node, index);
    py_children.insert(py_children.begin() + index, py_child);
}
/*
void Node::insertChild(Node* child, unsigned index) {
  YGNodeInsertChild(m_node, child->m_node, index);
}
*/
void Layout::addChild(py::object py_child) {
  // Extract C++ pointer from the Python object
  Layout* child = py_child.cast<Layout*>();
  YGNodeInsertChild(m_node, child->m_node, YGNodeGetChildCount(m_node));
  py_children.push_back(py_child);
}

void Layout::removeChild(Layout* child) {
  YGNodeRemoveChild(m_node, child->m_node);
}

unsigned Layout::getChildCount(void) const {
  return YGNodeGetChildCount(m_node);
}

Layout* Layout::getParent(void) {
  auto nodePtr = YGNodeGetParent(m_node);

  if (nodePtr == nullptr)
    return nullptr;

  return Layout::fromYGNode(nodePtr);
}

Layout* Layout::getChild(unsigned index) {
  auto nodePtr = YGNodeGetChild(m_node, index);

  if (nodePtr == nullptr)
    return nullptr;

  return Layout::fromYGNode(nodePtr);
}

void Layout::setMeasureFunc(MeasureCallback* measureFunc) {
  m_measureFunc.reset(measureFunc);

  YGNodeSetMeasureFunc(m_node, &globalMeasureFunc);
}

void Layout::unsetMeasureFunc(void) {
  m_measureFunc.reset(nullptr);

  YGNodeSetMeasureFunc(m_node, nullptr);
}

Size Layout::callMeasureFunc(
    double width,
    int widthMode,
    double height,
    int heightMode) const {
  return m_measureFunc->measure(width, widthMode, height, heightMode);
}

void Layout::setDirtiedFunc(DirtiedCallback* dirtiedFunc) {
  m_dirtiedFunc.reset(dirtiedFunc);

  YGNodeSetDirtiedFunc(m_node, &globalDirtiedFunc);
}

void Layout::unsetDirtiedFunc(void) {
  m_dirtiedFunc.reset(nullptr);

  YGNodeSetDirtiedFunc(m_node, nullptr);
}

void Layout::callDirtiedFunc(void) const {
  m_dirtiedFunc->dirtied();
}

void Layout::markDirty(void) {
  YGNodeMarkDirty(m_node);
}

bool Layout::isDirty(void) const {
  return YGNodeIsDirty(m_node);
}

void Layout::markLayoutSeen() {
  YGNodeSetHasNewLayout(m_node, false);
}

bool Layout::hasNewLayout(void) const {
  return YGNodeGetHasNewLayout(m_node);
}

//void Node::calculateLayout(double width, double height, int direction) {
void Layout::calculateBounds(double width, double height, facebook::yoga::Direction direction) {
  YGNodeCalculateLayout(
      m_node, width, height, static_cast<YGDirection>(direction));
}

double Layout::getComputedLeft(void) const {
  return YGNodeLayoutGetLeft(m_node);
}

double Layout::getComputedRight(void) const {
  return YGNodeLayoutGetRight(m_node);
}

double Layout::getComputedTop(void) const {
  return YGNodeLayoutGetTop(m_node);
}

double Layout::getComputedBottom(void) const {
  return YGNodeLayoutGetBottom(m_node);
}

double Layout::getComputedWidth(void) const {
  return YGNodeLayoutGetWidth(m_node);
}

double Layout::getComputedHeight(void) const {
  return YGNodeLayoutGetHeight(m_node);
}

Bounds Layout::getComputedBounds(void) const {
  Bounds layout;

  layout.left = YGNodeLayoutGetLeft(m_node);
  layout.right = YGNodeLayoutGetRight(m_node);

  layout.top = YGNodeLayoutGetTop(m_node);
  layout.bottom = YGNodeLayoutGetBottom(m_node);

  layout.width = YGNodeLayoutGetWidth(m_node);
  layout.height = YGNodeLayoutGetHeight(m_node);

  return layout;
}

double Layout::getComputedMargin(int edge) const {
  return YGNodeLayoutGetMargin(m_node, static_cast<YGEdge>(edge));
}

double Layout::getComputedBorder(int edge) const {
  return YGNodeLayoutGetBorder(m_node, static_cast<YGEdge>(edge));
}

double Layout::getComputedPadding(int edge) const {
  return YGNodeLayoutGetPadding(m_node, static_cast<YGEdge>(edge));
}

void Layout::setAlwaysFormsContainingBlock(bool alwaysFormsContainingBlock) {
  return YGNodeSetAlwaysFormsContainingBlock(
      m_node, alwaysFormsContainingBlock);
}
