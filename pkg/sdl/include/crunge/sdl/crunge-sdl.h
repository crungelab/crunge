#include <SDL3/SDL.h>

class SDLWindowWrapper {
public:
    //SDLWindowWrapper(SDL_Window *window);
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

/*struct SDL_Window {
    int _;
};*/


