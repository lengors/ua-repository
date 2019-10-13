
## BUILD ##
./build.sh

## RUN ##

FCM:
./run fcm [k] [alpha] [text='test.txt'] [model='model.mdl']

GENERATOR:
./run generator [-s max_size] [-t initial_text] [-o output_model_filename] [-p] [input_model_filename='model.mdl']