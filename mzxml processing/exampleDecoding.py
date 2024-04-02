import base64
import struct

'''
An example of a scan's peak data is:
<scan num="1" msLevel="1" peaksCount="518" polarity="+" scanType="CID" filterLine="FTMS + p ESI Full ms [70.0000-1000.0000]" retentionTime="PT0.192148158S" lowMz="70.0292282104492" highMz="674.198913574219" basePeakMz="123.0789206" basePeakIntensity="43500976" totIonCurrent="109587810">
	<peaks precision="32" byteOrder="network" pairOrder="m/z-int">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</peaks>
</scan>
'''

text = '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'

#Decode from base64-encoded string to bytes
decoded = base64.b64decode(text)

# Unpack the bytes into a list of floats
format_string = '!' + 'f' * (len(decoded) // 4)
'''
Format String explanation:
! - big-endian byte order
f - floats (32-bit)
len(decoded) // 4 - number of floats in the byte array. Total len divided by 4 because a 32-bit float is 4 bytes long
'''

idx = 0
mz_list = []
intensity_list = []
for val in struct.unpack_from(format_string, decoded):
    if(idx%2 == 0):
        mz_list.append(float(val))
    else:
        intensity_list.append(float(val))
    idx += 1

print(mz_list[0])
print(intensity_list[0])