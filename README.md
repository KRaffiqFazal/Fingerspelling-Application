# BSL Fingerspelling Proof of Concept Application

## Description
This is a final-year Applied Computer Science BSc project that uses MediaPipe hand landmarks and a gesture recogniser model to classify the BSL fingerspelling Alphabet.

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/KRaffiqFazal/Fingerspelling-Application.git
   ```
2. Install required packages
   ```sh
   pip install opencv-python
   pip install mediapipe
   ```

## Usage
Letters can be classified from a live camera feed with [this](Live-Feed-Recognition.py). This serves as a proof of concept example that relies on logic present [here](GestureMethods.py).
