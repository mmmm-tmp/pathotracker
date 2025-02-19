for sp in {1..93}; do
    echo ${sp}
    cd ./cluster${sp}
    python pan_count.py
    cd ..
done
