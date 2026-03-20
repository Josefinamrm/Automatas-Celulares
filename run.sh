rm -rf particles_frames.txt
cd java
javac -cp *.java
java App 100 10 5 1 true 500 3 0
cd ..
python3 visualize.py