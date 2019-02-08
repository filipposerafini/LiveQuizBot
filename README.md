# LiveQuizBot ![Python][python] [![License](https://img.shields.io/badge/License-MIT-red.svg?longCache=true&style=flat-square)](LICENSE)

> A Python Bot that tries to suggest you answers to [LiveQuiz](https://play.google.com/store/apps/details?id=com.bendingspoons.live.quiz) questions.

:construction:

I still have to work on the accuracy that as of today is pretty low :sweat_smile:

For now is working only on smartphone with a resolution of 2246x1080, but I'm willing to make it device independant.

:construction:

### Disclaimer

I don't encourage anyone to use this bot, that was made exclusively for educational purposes.

## Requirements

The script requires `adb`, available within the [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools).

To install the other requirements: `pip install -r requirements.txt`.

## Usage

1. Enable USB debugging on your smartphone.
2. Plug the phone and check, using `adb devices`, if your device is listed.
3. Run `python answer_bot.py`.
4. As soon as the question is shown press `Enter` to take a screenshot and wait few seconds for the processing.
5. **Good Luck!**

## License

Distributed under the [MIT](LICENSE) license.

Copyright &copy; 2019, [Filippo Serafini](https://filipposerafini.github.io/).

[python]: https://img.shields.io/badge/python-3-blue.svg?longCache=true&style=flat-square
