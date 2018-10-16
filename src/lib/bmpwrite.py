from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from struct import pack
import vtk


class BmpWriter(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(
            self, nInputPorts=1, inputType='vtkImageData')

        self._file_name = "default.bmp"

    def set_file_name(self, name):
        self._file_name = name

    def find_closest_color(self, old_val):
        return round(old_val/255)*255

    def append_error(self, img, i, j, error):
        old_val = img.GetScalarComponentAsFloat(i, j, 0, 0)
        new_val = old_val + error
        img.SetScalarComponentFromFloat(i, j, 0, 0, new_val)

    def RequestData(self, request, inInfo, outInfo):
        inp = vtk.vtkImageData.GetData(inInfo[0])

        dim = inp.GetDimensions()

        f = open(self._file_name, 'wb')
        bmp_header_size = 14
        dib_header_size = 40

        #in bit
        line_size = dim[0]
        padding = 32 - dim[0]%32

        #in bytes
        total_line_size = int((line_size + padding)/8)

        a_size = total_line_size*dim[1]
        total_size = bmp_header_size + dib_header_size + a_size
        a_offset = bmp_header_size + dib_header_size
        # BMP header
        f.write(pack('<HLHHL',
                     19778,
                     total_size,
                     0,
                     0,
                     a_offset))
        # DIB Header
        f.write(pack('<LllHHLLllLL',
                     dib_header_size,
                     dim[0],
                     dim[1],
                     1,
                     1,
                     0,
                     line_size*dim[1],
                     23622,
                     23622,
                     0,
                     0))

        # RGBQUAD Array
        f.write(pack('<BBBB', 255, 255, 255, 0))

        extent = inp.GetExtent()

        # write image
        for i in range(extent[0], extent[1]+1):
            bit_row = ""
            for j in range(extent[2], extent[3]+1):
                old_val = inp.GetScalarComponentAsFloat(i, j, 0, 0)
                new_val = self.find_closest_color(old_val)

                inp.SetScalarComponentFromFloat(i, j, 0, 0, new_val)

                quant_error = old_val-new_val

                if((i+1) <= extent[1] and quant_error != 0 ):
                    self.append_error(inp, i+1, j, quant_error*7/16)

                if ((i-1) >= extent[0] and (j+1) <= extent[3] and quant_error != 0):
                    self.append_error(inp, i-1, j, quant_error*3/16)

                if ((j+1) <= extent[3] and quant_error != 0):
                    self.append_error(inp, i, j+1, quant_error*5/16)

                if ((i+1) <= extent[1] and (j+1) <= extent[3] and quant_error != 0):
                    self.append_error(inp, i, j+1, quant_error*1/16)
                
                if(new_val == 255):
                    bit_row += "1"
                else:
                    bit_row += "0"
                
                if(len(bit_row) == 31):
                    f.write(pack('<i', int(bit_row[::-1], base=2)))
                    bit_row = ""

            bit_row += padding*"0"
            f.write(pack('<i', int(bit_row[::-1], base=2)))
    
        f.close()

        return 1