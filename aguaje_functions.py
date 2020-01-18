import numpy as np
import os
import cv2
import gdal
from keras.models import load_model
import keras.backend as K

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

K.set_image_data_format('channels_last')
K.set_learning_phase(0)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Metric
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def build_aguaje():
    def relu6(x):
        return K.relu(x, max_value=6)

    model = load_model("Redes/Final_DeeplabG1.h5", custom_objects={'relu6': relu6})

    return model


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
LECTURA IMAGEN
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def detectaguaje(folder, filename):
    from keras.backend import clear_session
    clear_session()

    Im = cv2.imread(filename)
    b, g, r = cv2.split(Im)
    Im = cv2.merge([r, g, b])
    Im = Im.astype(np.uint8)

    [M, N, P] = Im.shape

    if M >= 4000 and N >= 6000 and P == 3:
        Im = cv2.resize(Im, (3000, 2000))

    n1 = int(np.floor(Im.shape[0] / 512))  # nro segmentos en X
    s1 = int(np.floor(Im.shape[0] / n1))  # Paso en X
    n2 = int(np.floor(Im.shape[1] / 512))  # nro segmentos en Y
    s2 = int(np.floor(Im.shape[1] / n2))  # Paso en Y

    Blocks = np.zeros((n1 * n2, 512, 512, 3)).astype(np.uint8)

    cnt = 0

    for x in range(0, n1):
        for y in range(0, n2):

            if x == n1 and y != n2:
                Blocks[cnt] = cv2.resize(Im[s1 * x - 50:, s2 * y - 50:(s2 * (y + 1)), :], (512, 512))
            elif x != n1 and y == n2:
                Blocks[cnt] = cv2.resize(Im[s1 * x - 50:(s1 * (x + 1)), s2 * y - 50:, :], (512, 512))
            elif x == n1 and y == n2:
                Blocks[cnt] = cv2.resize(Im[s1 * x - 50:, s2 * y - 50:, :], (512, 512))
            elif x == 0 and y == 0:
                Blocks[cnt] = cv2.resize(Im[s1 * x:(s1 * (x + 1)), s2 * y:(s2 * (y + 1)), :], (512, 512))
            elif x == 0 and y != 0:
                Blocks[cnt] = cv2.resize(Im[s1 * x:(s1 * (x + 1)), s2 * y - 50:(s2 * (y + 1)), :], (512, 512))
            elif x != 0 and y == 0:
                Blocks[cnt] = cv2.resize(Im[s1 * x - 50:(s1 * (x + 1)), s2 * y:(s2 * (y + 1)), :], (512, 512))
            else:
                Blocks[cnt] = cv2.resize(Im[s1 * x - 50:(s1 * (x + 1)), s2 * y - 50:(s2 * (y + 1)), :], (512, 512))

            cnt = cnt + 1

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    APLICA CNN
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    model = build_aguaje()

    r = []
    for u in range(0, (n1 * n2) // 5 + 1):
        if u + 1 == (n1 * n2) // 5 + 1:
            rtemp = model.predict(Blocks[u * 5:])
        else:
            rtemp = model.predict(Blocks[u * 5:u * 5 + 5])

        for uu in range(0, len(rtemp)):
            r.append(rtemp[uu])

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    ARMA MAPA
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    maskf = np.zeros((Im.shape[0], Im.shape[1]), dtype=np.uint8)
    cnt = 0
    for x in range(0, n1):
        for y in range(0, n2):

            if x == n1 and y != n2:
                m = maskf[s1 * x - 50:, s2 * y - 50:(s2 * (y + 1))]
                [h, w] = m.shape
                maskf[s1 * x - 50:, s2 * y - 50:(s2 * (y + 1))] = np.maximum(m, cv2.resize(
                    np.reshape(r[cnt], (512, 512)), (w, h)) * 255)
            elif x != n1 and y == n2:
                m = maskf[s1 * x - 50:(s1 * (x + 1)), s2 * y - 50:]
                [h, w] = m.shape
                maskf[s1 * x - 50:(s1 * (x + 1)), s2 * y - 50:] = np.maximum(m, cv2.resize(
                    np.reshape(r[cnt], (512, 512)), (w, h)) * 255)
            elif x == n1 and y == n2:
                m = maskf[s1 * x - 50:, s2 * y - 50:]
                [h, w] = m.shape
                maskf[s1 * x - 50:, s2 * y - 50:] = np.maximum(m, cv2.resize(np.reshape(r[cnt], (512, 512)),
                                                                             (w, h)) * 255)
            elif x == 0 and y == 0:
                m = maskf[s1 * x:(s1 * (x + 1)), s2 * y:(s2 * (y + 1))]
                [h, w] = m.shape
                maskf[s1 * x:(s1 * (x + 1)), s2 * y:(s2 * (y + 1))] = np.maximum(m, cv2.resize(
                    np.reshape(r[cnt], (512, 512)), (w, h)) * 255)
            elif x == 0 and y != 0:
                m = maskf[s1 * x:(s1 * (x + 1)), s2 * y - 50:(s2 * (y + 1))]
                [h, w] = m.shape
                maskf[s1 * x:(s1 * (x + 1)), s2 * y - 50:(s2 * (y + 1))] = np.maximum(m, cv2.resize(
                    np.reshape(r[cnt], (512, 512)), (w, h)) * 255)
            elif x != 0 and y == 0:
                m = maskf[s1 * x - 50:(s1 * (x + 1)), s2 * y:(s2 * (y + 1))]
                [h, w] = m.shape
                maskf[s1 * x - 50:(s1 * (x + 1)), s2 * y:(s2 * (y + 1))] = np.maximum(m, cv2.resize(
                    np.reshape(r[cnt], (512, 512)), (w, h)) * 255)
            else:
                m = maskf[s1 * x - 50:(s1 * (x + 1)), s2 * y - 50:(s2 * (y + 1))]
                [h, w] = m.shape
                maskf[s1 * x - 50:(s1 * (x + 1)), s2 * y - 50:(s2 * (y + 1))] = np.maximum(m, cv2.resize(
                    np.reshape(r[cnt], (512, 512)), (w, h)) * 255)

            cnt = cnt + 1

    # Apply threshold
    maskf = ((maskf > 205) * 255).astype(np.uint8)
    # Find connected components
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(maskf, connectivity=8)
    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    # Removes objects with less than min_size pixels
    min_size = 800
    maskf2 = np.zeros(maskf.shape)
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            maskf2[output == i + 1] = 1

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    GEORREFERENCIACION
    """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    print("Se procesó imagen: " + filename)
    #    print(folder)
    ds_ms = gdal.Open(filename)
    rojms = ds_ms.GetProjectionRef()
    ggtf = ds_ms.GetGeoTransform()
    driver = gdal.GetDriverByName("GTiff")
    if not os.path.isdir(folder + '\\Resultados'):
        os.makedirs(folder + '\\Resultados')
    outdata = driver.Create(folder + '\\Resultados\\' + filename[len(folder):-4] + '_mask.tif', N, M, 1, gdal.GDT_Byte,
                            ['NBITS=1'])
    outdata.SetGeoTransform(ggtf)
    outdata.SetProjection(rojms)
    maskf2 = cv2.resize(maskf2, (N, M))
    outdata.GetRasterBand(1).WriteArray(maskf2)
    outdata.GetRasterBand(1).SetNoDataValue(0)
    outdata.FlushCache()
