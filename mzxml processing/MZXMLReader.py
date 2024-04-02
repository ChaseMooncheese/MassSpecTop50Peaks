import base64
import struct


class Scan:
    def __init__(self, mz_list, intensity_list):
        self.mz_list = mz_list
        self.intensity_list = intensity_list
        self.elems: list[MZ_Intensity_Pair] = [MZ_Intensity_Pair(mz, intensity) for mz, intensity in zip(mz_list, intensity_list)]

    def get_mz_list(self):
        return self.mz_list

    def get_intensity_list(self):
        return self.intensity_list


class MZ_Intensity_Pair:
    def __init__(self, mz, intensity):
        self.mz = mz
        self.intensity = intensity


class MZXMLReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.scan_number = 1
        self.line_number = 0

    def get_scans(self):
        scans = []
        with open(self.file_path, 'r') as file:
            text = file.read()
            lines = text.splitlines()

            while self.line_number < len(lines):
                # Read the next scan and store its mz_list and intensity_list
                scan = self.process_next_scan(lines)
                if not scan:
                    return scans
                scans.append(scan)

    def process_next_scan(self, lines):
        scan_open_tag = self.read_until_scan_open_tag(lines)

        if not scan_open_tag:
            return None

        self.line_number += 1
        scan_peak_tag = self.read_until_scan_peak_tag(lines)
        raw_base64_encoded_string = self.get_raw_peak_data(scan_peak_tag)
        scan_close_tag = self.read_until_scan_close_tag(lines)

        mz_list, intensity_list = self.decode_raw(raw_base64_encoded_string)
        return Scan(mz_list, intensity_list)

    def read_until_scan_open_tag(self, lines):
        while self.line_number < len(lines):
            line = lines[self.line_number]
            if "<scan" in line:
                return line
            self.line_number += 1

    def read_until_scan_close_tag(self, lines):
        while self.line_number < len(lines):
            line = lines[self.line_number]
            if "</scan" in line:
                return line
            self.line_number += 1

    def read_until_scan_peak_tag(self, lines):
        while self.line_number < len(lines):
            line = lines[self.line_number]
            if "<peaks" in line:
                return line
            self.line_number += 1
        pass

    def decode_raw(self, raw_base64_encoded_string):
        # Decode from base64-encoded string to bytes
        decoded = base64.b64decode(raw_base64_encoded_string)

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
            if idx % 2 == 0:
                mz_list.append(float(val))
            else:
                intensity_list.append(float(val))
            idx += 1

        return mz_list, intensity_list

    def get_raw_peak_data(self, peak_line):
        index = peak_line.find(">")
        index2 = peak_line.find("</peaks>")
        return peak_line[index + 1:index2]
