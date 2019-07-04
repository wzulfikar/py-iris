## Python Iris: Image Processing Library

- Python 3 only
- display all commands: `python iris.py`
- stream from video capture device and run thru the pipelines: `python iris.py stream`
- comment `disable_pipelines` in app config (eg. app.sample.yml) to enable all pipelines.

#### Usage

- install dependencies (macOS):

    ```
    brew install cmake opencv dlib
    ```

- init env & install python dependencies (use anaconda/miniconda):

    ```
    conda env create -f environment.yml
    conda activate py-iris
    pip install -r requirements.txt
    ```
- start stream using default webcam: 

    ```
    ./iris.py stream 0 app.sample.yml
    ```