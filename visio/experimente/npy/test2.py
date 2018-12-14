import npyscreen as np

def test(*args):
    F = np.Form(name='Hihi!')
    F.display()

if __name__ == '__main__':
    try:
        np.wrapper_basic(test)
    except KeyboardInterrupt:
        pass
