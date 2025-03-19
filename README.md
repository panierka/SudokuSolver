# SudokuSolver
The main task of Machine Learning Applications in human-machine interaction systems course on second semester (MSc) at Silesian University of Technology was to create application that lets the users get solved sudoku system automatically using their mobile phone.

Our team succesfully delivered mobile application which is able to:
- take the photo of paper sudoku board,
- process the image and detect digits,
- solve the formed sudoku board,
- return the solution or inform the user about incorrect input (illogical digits setup on the board).

Vital parts of application included sudoku solving algorithm and Machine Learning model detecting digits - CNN using LeNet-5 architecture trained on [SVHN cropped](http://ufldl.stanford.edu/housenumbers/) dataset.

The technology scope:

- client - mobile app created in Unity using C# scripts,
  
- server - written in Python (used packages included Numpy, OpenCV, Tensorflow).


The team worked in given squad:
- [panierka](https://github.com/panierka) - API preparing, images processing, empty fields detection, executing and sending images using Unity,
- [jdylik](https://github.com/jdylik) - development of model of detecting digits on images, documentation, 
- [TR1PL3D0T](https://github.com/TR1PL3D0T) - sudoku solving algorithm, Docker configuration.

