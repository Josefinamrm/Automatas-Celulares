rm -rf particles_frames.txt va_vs_time.png
cd java
javac *.java
#java App <N> <L> <M> <rc> <periodic> <iterations> <eta> <withLeader> <leaderID> <circleLeader>
java App 400 10 5 1 true 100 0.0 true 0 false 
cd ..
if [ "$1" == "T" ]; then
    rm -rf output.gif
    python3 vis_thom.py
else
    python3 visualize.py
fi
python3 plot_va.py

#magic line to delete everything in /results: 
#find results/ -name "particles_frames.txt" -delete
