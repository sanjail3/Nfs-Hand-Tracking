
from control_keys import W, A, S, D
from control_keys import PressKey, ReleaseKey

class Control:
    current_key_pressed = set()

    def startControlling(self,controll):
        keyPressed = False
        keyPressed_lr = False
        recentKey = None

        if controll=='W':
            PressKey(W)
            recentKey = W
            print('Press W')
            keyPressed = True
            self.current_key_pressed.add(W)
        elif controll=='S':
            PressKey(S)
            recentKey = S
            print('Press S')
            keyPressed = True
            self.current_key_pressed.add(S)

        if controll=='A':
            PressKey(A)
            print('Press <--')
            self.current_key_pressed.add(A)
            keyPressed = True
            keyPressed_lr = True
        elif controll=='D':
            PressKey(D)
            print('Press -->')
            self.current_key_pressed.add(D)
            keyPressed = True
            keyPressed_lr = True

        if keyPressed:
            if recentKey == W and S in self.current_key_pressed:
                self.current_key_pressed.remove(S)
                ReleaseKey(S)

            elif recentKey == S and W in self.current_key_pressed:
                self.current_key_pressed.remove(W)
                ReleaseKey(W)

        if not keyPressed and len(self.current_key_pressed) != 0:
            for key in self.current_key_pressed:
                ReleaseKey(key)
                print('Release')
            self.current_key_pressed = set()

        if not keyPressed_lr and ((A in self.current_key_pressed) or (D in self.current_key_pressed)):
            if A in self.current_key_pressed:
                ReleaseKey(A)
                self.current_key_pressed.remove(A)
            elif D in self.current_key_pressed:
                ReleaseKey(D)
                self.current_key_pressed.remove(D)