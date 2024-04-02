from MZXMLReader import MZXMLReader, Scan

file_path = "../data/ex.mzxml"


reader = MZXMLReader(file_path)

scans = reader.get_scans()
first_scan: Scan = scans[0]
# print(first_scan.get_mz_list())
# print()
# print()
# print(first_scan.get_intensity_list())


# Sort by intensity
pairs_sorted_by_intensity = sorted(first_scan.elems, key=lambda x: x.intensity, reverse=True)[0:50]
print('\tM/Z \t\t\t\tIntensity')
for i, elem in enumerate(pairs_sorted_by_intensity):
    print(str(i+1) + '.\t' + str(elem.mz) + '\t' + str(elem.intensity))

# pairs_sorted = sorted(zip(first_scan.get_intensity_list(), first_scan.get_mz_list()), reverse=True)[0:50]
# for i, elem in enumerate(pairs_sorted):
#     print(str(i) + '.\t' + str(elem[1]) + '\t' + str(elem[0]))




