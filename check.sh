total_size=0
for package in $(pip freeze | cut -d'=' -f1); do
    size=$(pip show $package | grep "Size: " | awk '{print $2}')
    total_size=$((total_size + size))
done

echo "Total size of installed packages: $total_size KB"

