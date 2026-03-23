if [ -f "particles_frames.txt" ]; then
    echo "Removing existing particles_frames.txt"
    rm -rf particles_frames.txt
fi
cd java
javac *.java
#java App <N> <L> <M> <rc> <periodic> <iterations> <eta> <leaderID> <circleLeader>
java App 400 10 5 1 true 500 0.0 0 true
cd ..
if [ "$1" == "T" ]; then
    rm -rf output.gif
    python3 vis_thom.py
else
    python3 visualize.py
fi