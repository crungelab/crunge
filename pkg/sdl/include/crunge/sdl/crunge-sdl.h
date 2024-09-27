#include <SDL3/SDL.h>

template<typename T>
class Wrapper {
public:
    Wrapper(T* value) : value(value) {}

    ~Wrapper() {
        // Add custom resource deallocation if needed, like SDL_DestroyWindow for SDL_Window
    }

    // Implicit conversion operator to T*
    operator T*() const {
        return value;
    }

    T* get() const {
        return value;
    }

    // Add more functionality as needed

private:
    T* value;
};

using SDLWindowWrapper = Wrapper<SDL_Window>;
/*class SDLWindowWrapper : public Wrapper<SDL_Window> {
};*/
using SDLCursorWrapper = Wrapper<SDL_Cursor>;
/*class SDLCursorWrapper : public Wrapper<SDL_Cursor> {
};*/

/*class SDLWindowWrapper {
public:
    SDLWindowWrapper(SDL_Window *window) : window(window) {}

    ~SDLWindowWrapper() {
    }

    SDL_Window* get() const {
        return window;
    }

    // Add more functionality as needed

private:
    SDL_Window *window;
};

class SDLCursorWrapper {
public:
    SDLCursorWrapper(SDL_Cursor *cursor) : cursor(cursor) {}

    ~SDLCursorWrapper() {
    }

    SDL_Cursor* get() const {
        return cursor;
    }

    // Add more functionality as needed

private:
    SDL_Cursor *cursor;
};*/
