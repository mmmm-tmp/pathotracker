for sp in {1..93}; do
        cd ./cluster${sp}
        python isolatename_from_csv.py
        cd ..
done
