import sys
from six import StringIO

import pandas as pd

# Table of MODIS tile bounding coordinates from https://modis-land.gsfc.nasa.gov/pdf/sn_bound_10deg.txt
SINOSOIDAL_GRID_COORDINATES_STRING = """
iv  ih    lon_min    lon_max   lat_min   lat_max
  0   0  -999.0000  -999.0000  -99.0000  -99.0000
  0   1  -999.0000  -999.0000  -99.0000  -99.0000
  0   2  -999.0000  -999.0000  -99.0000  -99.0000
  0   3  -999.0000  -999.0000  -99.0000  -99.0000
  0   4  -999.0000  -999.0000  -99.0000  -99.0000
  0   5  -999.0000  -999.0000  -99.0000  -99.0000
  0   6  -999.0000  -999.0000  -99.0000  -99.0000
  0   7  -999.0000  -999.0000  -99.0000  -99.0000
  0   8  -999.0000  -999.0000  -99.0000  -99.0000
  0   9  -999.0000  -999.0000  -99.0000  -99.0000
  0  10  -999.0000  -999.0000  -99.0000  -99.0000
  0  11  -999.0000  -999.0000  -99.0000  -99.0000
  0  12  -999.0000  -999.0000  -99.0000  -99.0000
  0  13  -999.0000  -999.0000  -99.0000  -99.0000
  0  14  -180.0000  -172.7151   80.0000   80.4083
  0  15  -180.0000  -115.1274   80.0000   83.6250
  0  16  -180.0000   -57.5397   80.0000   86.8167
  0  17  -180.0000    57.2957   80.0000   90.0000
  0  18    -0.0040   180.0000   80.0000   90.0000
  0  19    57.5877   180.0000   80.0000   86.8167
  0  20   115.1754   180.0000   80.0000   83.6250
  0  21   172.7631   180.0000   80.0000   80.4083
  0  22  -999.0000  -999.0000  -99.0000  -99.0000
  0  23  -999.0000  -999.0000  -99.0000  -99.0000
  0  24  -999.0000  -999.0000  -99.0000  -99.0000
  0  25  -999.0000  -999.0000  -99.0000  -99.0000
  0  26  -999.0000  -999.0000  -99.0000  -99.0000
  0  27  -999.0000  -999.0000  -99.0000  -99.0000
  0  28  -999.0000  -999.0000  -99.0000  -99.0000
  0  29  -999.0000  -999.0000  -99.0000  -99.0000
  0  30  -999.0000  -999.0000  -99.0000  -99.0000
  0  31  -999.0000  -999.0000  -99.0000  -99.0000
  0  32  -999.0000  -999.0000  -99.0000  -99.0000
  0  33  -999.0000  -999.0000  -99.0000  -99.0000
  0  34  -999.0000  -999.0000  -99.0000  -99.0000
  0  35  -999.0000  -999.0000  -99.0000  -99.0000
  1   0  -999.0000  -999.0000  -99.0000  -99.0000
  1   1  -999.0000  -999.0000  -99.0000  -99.0000
  1   2  -999.0000  -999.0000  -99.0000  -99.0000
  1   3  -999.0000  -999.0000  -99.0000  -99.0000
  1   4  -999.0000  -999.0000  -99.0000  -99.0000
  1   5  -999.0000  -999.0000  -99.0000  -99.0000
  1   6  -999.0000  -999.0000  -99.0000  -99.0000
  1   7  -999.0000  -999.0000  -99.0000  -99.0000
  1   8  -999.0000  -999.0000  -99.0000  -99.0000
  1   9  -999.0000  -999.0000  -99.0000  -99.0000
  1  10  -999.0000  -999.0000  -99.0000  -99.0000
  1  11  -180.0000  -175.4039   70.0000   70.5333
  1  12  -180.0000  -146.1659   70.0000   73.8750
  1  13  -180.0000  -116.9278   70.0000   77.1667
  1  14  -180.0000   -87.6898   70.0000   80.0000
  1  15  -172.7631   -58.4517   70.0000   80.0000
  1  16  -115.1754   -29.2137   70.0000   80.0000
  1  17   -57.5877     0.0480   70.0000   80.0000
  1  18     0.0000    57.6357   70.0000   80.0000
  1  19    29.2380   115.2234   70.0000   80.0000
  1  20    58.4761   172.8111   70.0000   80.0000
  1  21    87.7141   180.0000   70.0000   80.0000
  1  22   116.9522   180.0000   70.0000   77.1583
  1  23   146.1902   180.0000   70.0000   73.8750
  1  24   175.4283   180.0000   70.0000   70.5333
  1  25  -999.0000  -999.0000  -99.0000  -99.0000
  1  26  -999.0000  -999.0000  -99.0000  -99.0000
  1  27  -999.0000  -999.0000  -99.0000  -99.0000
  1  28  -999.0000  -999.0000  -99.0000  -99.0000
  1  29  -999.0000  -999.0000  -99.0000  -99.0000
  1  30  -999.0000  -999.0000  -99.0000  -99.0000
  1  31  -999.0000  -999.0000  -99.0000  -99.0000
  1  32  -999.0000  -999.0000  -99.0000  -99.0000
  1  33  -999.0000  -999.0000  -99.0000  -99.0000
  1  34  -999.0000  -999.0000  -99.0000  -99.0000
  1  35  -999.0000  -999.0000  -99.0000  -99.0000
  2   0  -999.0000  -999.0000  -99.0000  -99.0000
  2   1  -999.0000  -999.0000  -99.0000  -99.0000
  2   2  -999.0000  -999.0000  -99.0000  -99.0000
  2   3  -999.0000  -999.0000  -99.0000  -99.0000
  2   4  -999.0000  -999.0000  -99.0000  -99.0000
  2   5  -999.0000  -999.0000  -99.0000  -99.0000
  2   6  -999.0000  -999.0000  -99.0000  -99.0000
  2   7  -999.0000  -999.0000  -99.0000  -99.0000
  2   8  -999.0000  -999.0000  -99.0000  -99.0000
  2   9  -180.0000  -159.9833   60.0000   63.6167
  2  10  -180.0000  -139.9833   60.0000   67.1167
  2  11  -180.0000  -119.9833   60.0000   70.0000
  2  12  -175.4283   -99.9833   60.0000   70.0000
  2  13  -146.1902   -79.9833   60.0000   70.0000
  2  14  -116.9522   -59.9833   60.0000   70.0000
  2  15   -87.7141   -39.9833   60.0000   70.0000
  2  16   -58.4761   -19.9833   60.0000   70.0000
  2  17   -29.2380     0.0244   60.0000   70.0000
  2  18     0.0000    29.2624   60.0000   70.0000
  2  19    20.0000    58.5005   60.0000   70.0000
  2  20    40.0000    87.7385   60.0000   70.0000
  2  21    60.0000   116.9765   60.0000   70.0000
  2  22    80.0000   146.2146   60.0000   70.0000
  2  23   100.0000   175.4526   60.0000   70.0000
  2  24   120.0000   180.0000   60.0000   70.0000
  2  25   140.0000   180.0000   60.0000   67.1167
  2  26   160.0000   180.0000   60.0000   63.6167
  2  27  -999.0000  -999.0000  -99.0000  -99.0000
  2  28  -999.0000  -999.0000  -99.0000  -99.0000
  2  29  -999.0000  -999.0000  -99.0000  -99.0000
  2  30  -999.0000  -999.0000  -99.0000  -99.0000
  2  31  -999.0000  -999.0000  -99.0000  -99.0000
  2  32  -999.0000  -999.0000  -99.0000  -99.0000
  2  33  -999.0000  -999.0000  -99.0000  -99.0000
  2  34  -999.0000  -999.0000  -99.0000  -99.0000
  2  35  -999.0000  -999.0000  -99.0000  -99.0000
  3   0  -999.0000  -999.0000  -99.0000  -99.0000
  3   1  -999.0000  -999.0000  -99.0000  -99.0000
  3   2  -999.0000  -999.0000  -99.0000  -99.0000
  3   3  -999.0000  -999.0000  -99.0000  -99.0000
  3   4  -999.0000  -999.0000  -99.0000  -99.0000
  3   5  -999.0000  -999.0000  -99.0000  -99.0000
  3   6  -180.0000  -171.1167   50.0000   52.3333
  3   7  -180.0000  -155.5594   50.0000   56.2583
  3   8  -180.0000  -140.0022   50.0000   60.0000
  3   9  -180.0000  -124.4449   50.0000   60.0000
  3  10  -160.0000  -108.8877   50.0000   60.0000
  3  11  -140.0000   -93.3305   50.0000   60.0000
  3  12  -120.0000   -77.7732   50.0000   60.0000
  3  13  -100.0000   -62.2160   50.0000   60.0000
  3  14   -80.0000   -46.6588   50.0000   60.0000
  3  15   -60.0000   -31.1015   50.0000   60.0000
  3  16   -40.0000   -15.5443   50.0000   60.0000
  3  17   -20.0000     0.0167   50.0000   60.0000
  3  18     0.0000    20.0167   50.0000   60.0000
  3  19    15.5572    40.0167   50.0000   60.0000
  3  20    31.1145    60.0167   50.0000   60.0000
  3  21    46.6717    80.0167   50.0000   60.0000
  3  22    62.2290   100.0167   50.0000   60.0000
  3  23    77.7862   120.0167   50.0000   60.0000
  3  24    93.3434   140.0167   50.0000   60.0000
  3  25   108.9007   160.0167   50.0000   60.0000
  3  26   124.4579   180.0000   50.0000   60.0000
  3  27   140.0151   180.0000   50.0000   60.0000
  3  28   155.5724   180.0000   50.0000   56.2500
  3  29   171.1296   180.0000   50.0000   52.3333
  3  30  -999.0000  -999.0000  -99.0000  -99.0000
  3  31  -999.0000  -999.0000  -99.0000  -99.0000
  3  32  -999.0000  -999.0000  -99.0000  -99.0000
  3  33  -999.0000  -999.0000  -99.0000  -99.0000
  3  34  -999.0000  -999.0000  -99.0000  -99.0000
  3  35  -999.0000  -999.0000  -99.0000  -99.0000
  4   0  -999.0000  -999.0000  -99.0000  -99.0000
  4   1  -999.0000  -999.0000  -99.0000  -99.0000
  4   2  -999.0000  -999.0000  -99.0000  -99.0000
  4   3  -999.0000  -999.0000  -99.0000  -99.0000
  4   4  -180.0000  -169.6921   40.0000   43.7667
  4   5  -180.0000  -156.6380   40.0000   48.1917
  4   6  -180.0000  -143.5839   40.0000   50.0000
  4   7  -171.1296  -130.5299   40.0000   50.0000
  4   8  -155.5724  -117.4758   40.0000   50.0000
  4   9  -140.0151  -104.4217   40.0000   50.0000
  4  10  -124.4579   -91.3676   40.0000   50.0000
  4  11  -108.9007   -78.3136   40.0000   50.0000
  4  12   -93.3434   -65.2595   40.0000   50.0000
  4  13   -77.7862   -52.2054   40.0000   50.0000
  4  14   -62.2290   -39.1513   40.0000   50.0000
  4  15   -46.6717   -26.0973   40.0000   50.0000
  4  16   -31.1145   -13.0432   40.0000   50.0000
  4  17   -15.5572     0.0130   40.0000   50.0000
  4  18     0.0000    15.5702   40.0000   50.0000
  4  19    13.0541    31.1274   40.0000   50.0000
  4  20    26.1081    46.6847   40.0000   50.0000
  4  21    39.1622    62.2419   40.0000   50.0000
  4  22    52.2163    77.7992   40.0000   50.0000
  4  23    65.2704    93.3564   40.0000   50.0000
  4  24    78.3244   108.9136   40.0000   50.0000
  4  25    91.3785   124.4709   40.0000   50.0000
  4  26   104.4326   140.0281   40.0000   50.0000
  4  27   117.4867   155.5853   40.0000   50.0000
  4  28   130.5407   171.1426   40.0000   50.0000
  4  29   143.5948   180.0000   40.0000   50.0000
  4  30   156.6489   180.0000   40.0000   48.1917
  4  31   169.7029   180.0000   40.0000   43.7583
  4  32  -999.0000  -999.0000  -99.0000  -99.0000
  4  33  -999.0000  -999.0000  -99.0000  -99.0000
  4  34  -999.0000  -999.0000  -99.0000  -99.0000
  4  35  -999.0000  -999.0000  -99.0000  -99.0000
  5   0  -999.0000  -999.0000  -99.0000  -99.0000
  5   1  -999.0000  -999.0000  -99.0000  -99.0000
  5   2  -180.0000  -173.1955   30.0000   33.5583
  5   3  -180.0000  -161.6485   30.0000   38.9500
  5   4  -180.0000  -150.1014   30.0000   40.0000
  5   5  -169.7029  -138.5544   30.0000   40.0000
  5   6  -156.6489  -127.0074   30.0000   40.0000
  5   7  -143.5948  -115.4604   30.0000   40.0000
  5   8  -130.5407  -103.9134   30.0000   40.0000
  5   9  -117.4867   -92.3664   30.0000   40.0000
  5  10  -104.4326   -80.8194   30.0000   40.0000
  5  11   -91.3785   -69.2724   30.0000   40.0000
  5  12   -78.3244   -57.7254   30.0000   40.0000
  5  13   -65.2704   -46.1784   30.0000   40.0000
  5  14   -52.2163   -34.6314   30.0000   40.0000
  5  15   -39.1622   -23.0844   30.0000   40.0000
  5  16   -26.1081   -11.5374   30.0000   40.0000
  5  17   -13.0541     0.0109   30.0000   40.0000
  5  18     0.0000    13.0650   30.0000   40.0000
  5  19    11.5470    26.1190   30.0000   40.0000
  5  20    23.0940    39.1731   30.0000   40.0000
  5  21    34.6410    52.2272   30.0000   40.0000
  5  22    46.1880    65.2812   30.0000   40.0000
  5  23    57.7350    78.3353   30.0000   40.0000
  5  24    69.2820    91.3894   30.0000   40.0000
  5  25    80.8290   104.4435   30.0000   40.0000
  5  26    92.3760   117.4975   30.0000   40.0000
  5  27   103.9230   130.5516   30.0000   40.0000
  5  28   115.4701   143.6057   30.0000   40.0000
  5  29   127.0171   156.6598   30.0000   40.0000
  5  30   138.5641   169.7138   30.0000   40.0000
  5  31   150.1111   180.0000   30.0000   40.0000
  5  32   161.6581   180.0000   30.0000   38.9417
  5  33   173.2051   180.0000   30.0000   33.5583
  5  34  -999.0000  -999.0000  -99.0000  -99.0000
  5  35  -999.0000  -999.0000  -99.0000  -99.0000
  6   0  -999.0000  -999.0000  -99.0000  -99.0000
  6   1  -180.0000  -170.2596   20.0000   27.2667
  6   2  -180.0000  -159.6178   20.0000   30.0000
  6   3  -173.2051  -148.9760   20.0000   30.0000
  6   4  -161.6581  -138.3342   20.0000   30.0000
  6   5  -150.1111  -127.6925   20.0000   30.0000
  6   6  -138.5641  -117.0507   20.0000   30.0000
  6   7  -127.0171  -106.4089   20.0000   30.0000
  6   8  -115.4701   -95.7671   20.0000   30.0000
  6   9  -103.9230   -85.1254   20.0000   30.0000
  6  10   -92.3760   -74.4836   20.0000   30.0000
  6  11   -80.8290   -63.8418   20.0000   30.0000
  6  12   -69.2820   -53.2000   20.0000   30.0000
  6  13   -57.7350   -42.5582   20.0000   30.0000
  6  14   -46.1880   -31.9165   20.0000   30.0000
  6  15   -34.6410   -21.2747   20.0000   30.0000
  6  16   -23.0940   -10.6329   20.0000   30.0000
  6  17   -11.5470     0.0096   20.0000   30.0000
  6  18     0.0000    11.5566   20.0000   30.0000
  6  19    10.6418    23.1036   20.0000   30.0000
  6  20    21.2836    34.6506   20.0000   30.0000
  6  21    31.9253    46.1976   20.0000   30.0000
  6  22    42.5671    57.7446   20.0000   30.0000
  6  23    53.2089    69.2917   20.0000   30.0000
  6  24    63.8507    80.8387   20.0000   30.0000
  6  25    74.4924    92.3857   20.0000   30.0000
  6  26    85.1342   103.9327   20.0000   30.0000
  6  27    95.7760   115.4797   20.0000   30.0000
  6  28   106.4178   127.0267   20.0000   30.0000
  6  29   117.0596   138.5737   20.0000   30.0000
  6  30   127.7013   150.1207   20.0000   30.0000
  6  31   138.3431   161.6677   20.0000   30.0000
  6  32   148.9849   173.2147   20.0000   30.0000
  6  33   159.6267   180.0000   20.0000   30.0000
  6  34   170.2684   180.0000   20.0000   27.2667
  6  35  -999.0000  -999.0000  -99.0000  -99.0000
  7   0  -180.0000  -172.6141   10.0000   19.1917
  7   1  -180.0000  -162.4598   10.0000   20.0000
  7   2  -170.2684  -152.3055   10.0000   20.0000
  7   3  -159.6267  -142.1513   10.0000   20.0000
  7   4  -148.9849  -131.9970   10.0000   20.0000
  7   5  -138.3431  -121.8427   10.0000   20.0000
  7   6  -127.7013  -111.6885   10.0000   20.0000
  7   7  -117.0596  -101.5342   10.0000   20.0000
  7   8  -106.4178   -91.3799   10.0000   20.0000
  7   9   -95.7760   -81.2257   10.0000   20.0000
  7  10   -85.1342   -71.0714   10.0000   20.0000
  7  11   -74.4924   -60.9171   10.0000   20.0000
  7  12   -63.8507   -50.7629   10.0000   20.0000
  7  13   -53.2089   -40.6086   10.0000   20.0000
  7  14   -42.5671   -30.4543   10.0000   20.0000
  7  15   -31.9253   -20.3001   10.0000   20.0000
  7  16   -21.2836   -10.1458   10.0000   20.0000
  7  17   -10.6418     0.0089   10.0000   20.0000
  7  18     0.0000    10.6506   10.0000   20.0000
  7  19    10.1543    21.2924   10.0000   20.0000
  7  20    20.3085    31.9342   10.0000   20.0000
  7  21    30.4628    42.5760   10.0000   20.0000
  7  22    40.6171    53.2178   10.0000   20.0000
  7  23    50.7713    63.8595   10.0000   20.0000
  7  24    60.9256    74.5013   10.0000   20.0000
  7  25    71.0799    85.1431   10.0000   20.0000
  7  26    81.2341    95.7849   10.0000   20.0000
  7  27    91.3884   106.4266   10.0000   20.0000
  7  28   101.5427   117.0684   10.0000   20.0000
  7  29   111.6969   127.7102   10.0000   20.0000
  7  30   121.8512   138.3520   10.0000   20.0000
  7  31   132.0055   148.9938   10.0000   20.0000
  7  32   142.1597   159.6355   10.0000   20.0000
  7  33   152.3140   170.2773   10.0000   20.0000
  7  34   162.4683   180.0000   10.0000   20.0000
  7  35   172.6225   180.0000   10.0000   19.1833
  8   0  -180.0000  -169.9917   -0.0000   10.0000
  8   1  -172.6225  -159.9917   -0.0000   10.0000
  8   2  -162.4683  -149.9917   -0.0000   10.0000
  8   3  -152.3140  -139.9917   -0.0000   10.0000
  8   4  -142.1597  -129.9917   -0.0000   10.0000
  8   5  -132.0055  -119.9917   -0.0000   10.0000
  8   6  -121.8512  -109.9917   -0.0000   10.0000
  8   7  -111.6969   -99.9917   -0.0000   10.0000
  8   8  -101.5427   -89.9917   -0.0000   10.0000
  8   9   -91.3884   -79.9917   -0.0000   10.0000
  8  10   -81.2341   -69.9917   -0.0000   10.0000
  8  11   -71.0799   -59.9917   -0.0000   10.0000
  8  12   -60.9256   -49.9917   -0.0000   10.0000
  8  13   -50.7713   -39.9917   -0.0000   10.0000
  8  14   -40.6171   -29.9917   -0.0000   10.0000
  8  15   -30.4628   -19.9917   -0.0000   10.0000
  8  16   -20.3085    -9.9917   -0.0000   10.0000
  8  17   -10.1543     0.0085   -0.0000   10.0000
  8  18     0.0000    10.1627   -0.0000   10.0000
  8  19    10.0000    20.3170   -0.0000   10.0000
  8  20    20.0000    30.4713   -0.0000   10.0000
  8  21    30.0000    40.6255   -0.0000   10.0000
  8  22    40.0000    50.7798   -0.0000   10.0000
  8  23    50.0000    60.9341   -0.0000   10.0000
  8  24    60.0000    71.0883   -0.0000   10.0000
  8  25    70.0000    81.2426   -0.0000   10.0000
  8  26    80.0000    91.3969   -0.0000   10.0000
  8  27    90.0000   101.5511   -0.0000   10.0000
  8  28   100.0000   111.7054   -0.0000   10.0000
  8  29   110.0000   121.8597   -0.0000   10.0000
  8  30   120.0000   132.0139   -0.0000   10.0000
  8  31   130.0000   142.1682   -0.0000   10.0000
  8  32   140.0000   152.3225   -0.0000   10.0000
  8  33   150.0000   162.4767   -0.0000   10.0000
  8  34   160.0000   172.6310   -0.0000   10.0000
  8  35   170.0000   180.0000   -0.0000   10.0000
  9   0  -180.0000  -169.9917  -10.0000   -0.0000
  9   1  -172.6225  -159.9917  -10.0000   -0.0000
  9   2  -162.4683  -149.9917  -10.0000   -0.0000
  9   3  -152.3140  -139.9917  -10.0000   -0.0000
  9   4  -142.1597  -129.9917  -10.0000   -0.0000
  9   5  -132.0055  -119.9917  -10.0000   -0.0000
  9   6  -121.8512  -109.9917  -10.0000   -0.0000
  9   7  -111.6969   -99.9917  -10.0000   -0.0000
  9   8  -101.5427   -89.9917  -10.0000   -0.0000
  9   9   -91.3884   -79.9917  -10.0000   -0.0000
  9  10   -81.2341   -69.9917  -10.0000   -0.0000
  9  11   -71.0799   -59.9917  -10.0000   -0.0000
  9  12   -60.9256   -49.9917  -10.0000   -0.0000
  9  13   -50.7713   -39.9917  -10.0000   -0.0000
  9  14   -40.6171   -29.9917  -10.0000   -0.0000
  9  15   -30.4628   -19.9917  -10.0000   -0.0000
  9  16   -20.3085    -9.9917  -10.0000   -0.0000
  9  17   -10.1543     0.0085  -10.0000   -0.0000
  9  18     0.0000    10.1627  -10.0000   -0.0000
  9  19    10.0000    20.3170  -10.0000   -0.0000
  9  20    20.0000    30.4713  -10.0000   -0.0000
  9  21    30.0000    40.6255  -10.0000   -0.0000
  9  22    40.0000    50.7798  -10.0000   -0.0000
  9  23    50.0000    60.9341  -10.0000   -0.0000
  9  24    60.0000    71.0883  -10.0000   -0.0000
  9  25    70.0000    81.2426  -10.0000   -0.0000
  9  26    80.0000    91.3969  -10.0000   -0.0000
  9  27    90.0000   101.5511  -10.0000   -0.0000
  9  28   100.0000   111.7054  -10.0000   -0.0000
  9  29   110.0000   121.8597  -10.0000   -0.0000
  9  30   120.0000   132.0139  -10.0000   -0.0000
  9  31   130.0000   142.1682  -10.0000   -0.0000
  9  32   140.0000   152.3225  -10.0000   -0.0000
  9  33   150.0000   162.4767  -10.0000   -0.0000
  9  34   160.0000   172.6310  -10.0000   -0.0000
  9  35   170.0000   180.0000  -10.0000   -0.0000
 10   0  -180.0000  -172.6141  -19.1917  -10.0000
 10   1  -180.0000  -162.4598  -20.0000  -10.0000
 10   2  -170.2684  -152.3055  -20.0000  -10.0000
 10   3  -159.6267  -142.1513  -20.0000  -10.0000
 10   4  -148.9849  -131.9970  -20.0000  -10.0000
 10   5  -138.3431  -121.8427  -20.0000  -10.0000
 10   6  -127.7013  -111.6885  -20.0000  -10.0000
 10   7  -117.0596  -101.5342  -20.0000  -10.0000
 10   8  -106.4178   -91.3799  -20.0000  -10.0000
 10   9   -95.7760   -81.2257  -20.0000  -10.0000
 10  10   -85.1342   -71.0714  -20.0000  -10.0000
 10  11   -74.4924   -60.9171  -20.0000  -10.0000
 10  12   -63.8507   -50.7629  -20.0000  -10.0000
 10  13   -53.2089   -40.6086  -20.0000  -10.0000
 10  14   -42.5671   -30.4543  -20.0000  -10.0000
 10  15   -31.9253   -20.3001  -20.0000  -10.0000
 10  16   -21.2836   -10.1458  -20.0000  -10.0000
 10  17   -10.6418     0.0089  -20.0000  -10.0000
 10  18     0.0000    10.6506  -20.0000  -10.0000
 10  19    10.1543    21.2924  -20.0000  -10.0000
 10  20    20.3085    31.9342  -20.0000  -10.0000
 10  21    30.4628    42.5760  -20.0000  -10.0000
 10  22    40.6171    53.2178  -20.0000  -10.0000
 10  23    50.7713    63.8595  -20.0000  -10.0000
 10  24    60.9256    74.5013  -20.0000  -10.0000
 10  25    71.0799    85.1431  -20.0000  -10.0000
 10  26    81.2341    95.7849  -20.0000  -10.0000
 10  27    91.3884   106.4266  -20.0000  -10.0000
 10  28   101.5427   117.0684  -20.0000  -10.0000
 10  29   111.6969   127.7102  -20.0000  -10.0000
 10  30   121.8512   138.3520  -20.0000  -10.0000
 10  31   132.0055   148.9938  -20.0000  -10.0000
 10  32   142.1597   159.6355  -20.0000  -10.0000
 10  33   152.3140   170.2773  -20.0000  -10.0000
 10  34   162.4683   180.0000  -20.0000  -10.0000
 10  35   172.6225   180.0000  -19.1833  -10.0000
 11   0  -999.0000  -999.0000  -99.0000  -99.0000
 11   1  -180.0000  -170.2596  -27.2667  -20.0000
 11   2  -180.0000  -159.6178  -30.0000  -20.0000
 11   3  -173.2051  -148.9760  -30.0000  -20.0000
 11   4  -161.6581  -138.3342  -30.0000  -20.0000
 11   5  -150.1111  -127.6925  -30.0000  -20.0000
 11   6  -138.5641  -117.0507  -30.0000  -20.0000
 11   7  -127.0171  -106.4089  -30.0000  -20.0000
 11   8  -115.4701   -95.7671  -30.0000  -20.0000
 11   9  -103.9230   -85.1254  -30.0000  -20.0000
 11  10   -92.3760   -74.4836  -30.0000  -20.0000
 11  11   -80.8290   -63.8418  -30.0000  -20.0000
 11  12   -69.2820   -53.2000  -30.0000  -20.0000
 11  13   -57.7350   -42.5582  -30.0000  -20.0000
 11  14   -46.1880   -31.9165  -30.0000  -20.0000
 11  15   -34.6410   -21.2747  -30.0000  -20.0000
 11  16   -23.0940   -10.6329  -30.0000  -20.0000
 11  17   -11.5470     0.0096  -30.0000  -20.0000
 11  18     0.0000    11.5566  -30.0000  -20.0000
 11  19    10.6418    23.1036  -30.0000  -20.0000
 11  20    21.2836    34.6506  -30.0000  -20.0000
 11  21    31.9253    46.1976  -30.0000  -20.0000
 11  22    42.5671    57.7446  -30.0000  -20.0000
 11  23    53.2089    69.2917  -30.0000  -20.0000
 11  24    63.8507    80.8387  -30.0000  -20.0000
 11  25    74.4924    92.3857  -30.0000  -20.0000
 11  26    85.1342   103.9327  -30.0000  -20.0000
 11  27    95.7760   115.4797  -30.0000  -20.0000
 11  28   106.4178   127.0267  -30.0000  -20.0000
 11  29   117.0596   138.5737  -30.0000  -20.0000
 11  30   127.7013   150.1207  -30.0000  -20.0000
 11  31   138.3431   161.6677  -30.0000  -20.0000
 11  32   148.9849   173.2147  -30.0000  -20.0000
 11  33   159.6267   180.0000  -30.0000  -20.0000
 11  34   170.2684   180.0000  -27.2667  -20.0000
 11  35  -999.0000  -999.0000  -99.0000  -99.0000
 12   0  -999.0000  -999.0000  -99.0000  -99.0000
 12   1  -999.0000  -999.0000  -99.0000  -99.0000
 12   2  -180.0000  -173.1955  -33.5583  -30.0000
 12   3  -180.0000  -161.6485  -38.9500  -30.0000
 12   4  -180.0000  -150.1014  -40.0000  -30.0000
 12   5  -169.7029  -138.5544  -40.0000  -30.0000
 12   6  -156.6489  -127.0074  -40.0000  -30.0000
 12   7  -143.5948  -115.4604  -40.0000  -30.0000
 12   8  -130.5407  -103.9134  -40.0000  -30.0000
 12   9  -117.4867   -92.3664  -40.0000  -30.0000
 12  10  -104.4326   -80.8194  -40.0000  -30.0000
 12  11   -91.3785   -69.2724  -40.0000  -30.0000
 12  12   -78.3244   -57.7254  -40.0000  -30.0000
 12  13   -65.2704   -46.1784  -40.0000  -30.0000
 12  14   -52.2163   -34.6314  -40.0000  -30.0000
 12  15   -39.1622   -23.0844  -40.0000  -30.0000
 12  16   -26.1081   -11.5374  -40.0000  -30.0000
 12  17   -13.0541     0.0109  -40.0000  -30.0000
 12  18     0.0000    13.0650  -40.0000  -30.0000
 12  19    11.5470    26.1190  -40.0000  -30.0000
 12  20    23.0940    39.1731  -40.0000  -30.0000
 12  21    34.6410    52.2272  -40.0000  -30.0000
 12  22    46.1880    65.2812  -40.0000  -30.0000
 12  23    57.7350    78.3353  -40.0000  -30.0000
 12  24    69.2820    91.3894  -40.0000  -30.0000
 12  25    80.8290   104.4435  -40.0000  -30.0000
 12  26    92.3760   117.4975  -40.0000  -30.0000
 12  27   103.9230   130.5516  -40.0000  -30.0000
 12  28   115.4701   143.6057  -40.0000  -30.0000
 12  29   127.0171   156.6598  -40.0000  -30.0000
 12  30   138.5641   169.7138  -40.0000  -30.0000
 12  31   150.1111   180.0000  -40.0000  -30.0000
 12  32   161.6581   180.0000  -38.9417  -30.0000
 12  33   173.2051   180.0000  -33.5583  -30.0000
 12  34  -999.0000  -999.0000  -99.0000  -99.0000
 12  35  -999.0000  -999.0000  -99.0000  -99.0000
 13   0  -999.0000  -999.0000  -99.0000  -99.0000
 13   1  -999.0000  -999.0000  -99.0000  -99.0000
 13   2  -999.0000  -999.0000  -99.0000  -99.0000
 13   3  -999.0000  -999.0000  -99.0000  -99.0000
 13   4  -180.0000  -169.6921  -43.7667  -40.0000
 13   5  -180.0000  -156.6380  -48.1917  -40.0000
 13   6  -180.0000  -143.5839  -50.0000  -40.0000
 13   7  -171.1296  -130.5299  -50.0000  -40.0000
 13   8  -155.5724  -117.4758  -50.0000  -40.0000
 13   9  -140.0151  -104.4217  -50.0000  -40.0000
 13  10  -124.4579   -91.3676  -50.0000  -40.0000
 13  11  -108.9007   -78.3136  -50.0000  -40.0000
 13  12   -93.3434   -65.2595  -50.0000  -40.0000
 13  13   -77.7862   -52.2054  -50.0000  -40.0000
 13  14   -62.2290   -39.1513  -50.0000  -40.0000
 13  15   -46.6717   -26.0973  -50.0000  -40.0000
 13  16   -31.1145   -13.0432  -50.0000  -40.0000
 13  17   -15.5572     0.0130  -50.0000  -40.0000
 13  18     0.0000    15.5702  -50.0000  -40.0000
 13  19    13.0541    31.1274  -50.0000  -40.0000
 13  20    26.1081    46.6847  -50.0000  -40.0000
 13  21    39.1622    62.2419  -50.0000  -40.0000
 13  22    52.2163    77.7992  -50.0000  -40.0000
 13  23    65.2704    93.3564  -50.0000  -40.0000
 13  24    78.3244   108.9136  -50.0000  -40.0000
 13  25    91.3785   124.4709  -50.0000  -40.0000
 13  26   104.4326   140.0281  -50.0000  -40.0000
 13  27   117.4867   155.5853  -50.0000  -40.0000
 13  28   130.5407   171.1426  -50.0000  -40.0000
 13  29   143.5948   180.0000  -50.0000  -40.0000
 13  30   156.6489   180.0000  -48.1917  -40.0000
 13  31   169.7029   180.0000  -43.7583  -40.0000
 13  32  -999.0000  -999.0000  -99.0000  -99.0000
 13  33  -999.0000  -999.0000  -99.0000  -99.0000
 13  34  -999.0000  -999.0000  -99.0000  -99.0000
 13  35  -999.0000  -999.0000  -99.0000  -99.0000
 14   0  -999.0000  -999.0000  -99.0000  -99.0000
 14   1  -999.0000  -999.0000  -99.0000  -99.0000
 14   2  -999.0000  -999.0000  -99.0000  -99.0000
 14   3  -999.0000  -999.0000  -99.0000  -99.0000
 14   4  -999.0000  -999.0000  -99.0000  -99.0000
 14   5  -999.0000  -999.0000  -99.0000  -99.0000
 14   6  -180.0000  -171.1167  -52.3333  -50.0000
 14   7  -180.0000  -155.5594  -56.2583  -50.0000
 14   8  -180.0000  -140.0022  -60.0000  -50.0000
 14   9  -180.0000  -124.4449  -60.0000  -50.0000
 14  10  -160.0000  -108.8877  -60.0000  -50.0000
 14  11  -140.0000   -93.3305  -60.0000  -50.0000
 14  12  -120.0000   -77.7732  -60.0000  -50.0000
 14  13  -100.0000   -62.2160  -60.0000  -50.0000
 14  14   -80.0000   -46.6588  -60.0000  -50.0000
 14  15   -60.0000   -31.1015  -60.0000  -50.0000
 14  16   -40.0000   -15.5443  -60.0000  -50.0000
 14  17   -20.0000     0.0167  -60.0000  -50.0000
 14  18     0.0000    20.0167  -60.0000  -50.0000
 14  19    15.5572    40.0167  -60.0000  -50.0000
 14  20    31.1145    60.0167  -60.0000  -50.0000
 14  21    46.6717    80.0167  -60.0000  -50.0000
 14  22    62.2290   100.0167  -60.0000  -50.0000
 14  23    77.7862   120.0167  -60.0000  -50.0000
 14  24    93.3434   140.0167  -60.0000  -50.0000
 14  25   108.9007   160.0167  -60.0000  -50.0000
 14  26   124.4579   180.0000  -60.0000  -50.0000
 14  27   140.0151   180.0000  -60.0000  -50.0000
 14  28   155.5724   180.0000  -56.2500  -50.0000
 14  29   171.1296   180.0000  -52.3333  -50.0000
 14  30  -999.0000  -999.0000  -99.0000  -99.0000
 14  31  -999.0000  -999.0000  -99.0000  -99.0000
 14  32  -999.0000  -999.0000  -99.0000  -99.0000
 14  33  -999.0000  -999.0000  -99.0000  -99.0000
 14  34  -999.0000  -999.0000  -99.0000  -99.0000
 14  35  -999.0000  -999.0000  -99.0000  -99.0000
 15   0  -999.0000  -999.0000  -99.0000  -99.0000
 15   1  -999.0000  -999.0000  -99.0000  -99.0000
 15   2  -999.0000  -999.0000  -99.0000  -99.0000
 15   3  -999.0000  -999.0000  -99.0000  -99.0000
 15   4  -999.0000  -999.0000  -99.0000  -99.0000
 15   5  -999.0000  -999.0000  -99.0000  -99.0000
 15   6  -999.0000  -999.0000  -99.0000  -99.0000
 15   7  -999.0000  -999.0000  -99.0000  -99.0000
 15   8  -999.0000  -999.0000  -99.0000  -99.0000
 15   9  -180.0000  -159.9833  -63.6167  -60.0000
 15  10  -180.0000  -139.9833  -67.1167  -60.0000
 15  11  -180.0000  -119.9833  -70.0000  -60.0000
 15  12  -175.4283   -99.9833  -70.0000  -60.0000
 15  13  -146.1902   -79.9833  -70.0000  -60.0000
 15  14  -116.9522   -59.9833  -70.0000  -60.0000
 15  15   -87.7141   -39.9833  -70.0000  -60.0000
 15  16   -58.4761   -19.9833  -70.0000  -60.0000
 15  17   -29.2380     0.0244  -70.0000  -60.0000
 15  18     0.0000    29.2624  -70.0000  -60.0000
 15  19    20.0000    58.5005  -70.0000  -60.0000
 15  20    40.0000    87.7385  -70.0000  -60.0000
 15  21    60.0000   116.9765  -70.0000  -60.0000
 15  22    80.0000   146.2146  -70.0000  -60.0000
 15  23   100.0000   175.4526  -70.0000  -60.0000
 15  24   120.0000   180.0000  -70.0000  -60.0000
 15  25   140.0000   180.0000  -67.1167  -60.0000
 15  26   160.0000   180.0000  -63.6167  -60.0000
 15  27  -999.0000  -999.0000  -99.0000  -99.0000
 15  28  -999.0000  -999.0000  -99.0000  -99.0000
 15  29  -999.0000  -999.0000  -99.0000  -99.0000
 15  30  -999.0000  -999.0000  -99.0000  -99.0000
 15  31  -999.0000  -999.0000  -99.0000  -99.0000
 15  32  -999.0000  -999.0000  -99.0000  -99.0000
 15  33  -999.0000  -999.0000  -99.0000  -99.0000
 15  34  -999.0000  -999.0000  -99.0000  -99.0000
 15  35  -999.0000  -999.0000  -99.0000  -99.0000
 16   0  -999.0000  -999.0000  -99.0000  -99.0000
 16   1  -999.0000  -999.0000  -99.0000  -99.0000
 16   2  -999.0000  -999.0000  -99.0000  -99.0000
 16   3  -999.0000  -999.0000  -99.0000  -99.0000
 16   4  -999.0000  -999.0000  -99.0000  -99.0000
 16   5  -999.0000  -999.0000  -99.0000  -99.0000
 16   6  -999.0000  -999.0000  -99.0000  -99.0000
 16   7  -999.0000  -999.0000  -99.0000  -99.0000
 16   8  -999.0000  -999.0000  -99.0000  -99.0000
 16   9  -999.0000  -999.0000  -99.0000  -99.0000
 16  10  -999.0000  -999.0000  -99.0000  -99.0000
 16  11  -180.0000  -175.4039  -70.5333  -70.0000
 16  12  -180.0000  -146.1659  -73.8750  -70.0000
 16  13  -180.0000  -116.9278  -77.1667  -70.0000
 16  14  -180.0000   -87.6898  -80.0000  -70.0000
 16  15  -172.7631   -58.4517  -80.0000  -70.0000
 16  16  -115.1754   -29.2137  -80.0000  -70.0000
 16  17   -57.5877     0.0480  -80.0000  -70.0000
 16  18     0.0000    57.6357  -80.0000  -70.0000
 16  19    29.2380   115.2234  -80.0000  -70.0000
 16  20    58.4761   172.8111  -80.0000  -70.0000
 16  21    87.7141   180.0000  -80.0000  -70.0000
 16  22   116.9522   180.0000  -77.1583  -70.0000
 16  23   146.1902   180.0000  -73.8750  -70.0000
 16  24   175.4283   180.0000  -70.5333  -70.0000
 16  25  -999.0000  -999.0000  -99.0000  -99.0000
 16  26  -999.0000  -999.0000  -99.0000  -99.0000
 16  27  -999.0000  -999.0000  -99.0000  -99.0000
 16  28  -999.0000  -999.0000  -99.0000  -99.0000
 16  29  -999.0000  -999.0000  -99.0000  -99.0000
 16  30  -999.0000  -999.0000  -99.0000  -99.0000
 16  31  -999.0000  -999.0000  -99.0000  -99.0000
 16  32  -999.0000  -999.0000  -99.0000  -99.0000
 16  33  -999.0000  -999.0000  -99.0000  -99.0000
 16  34  -999.0000  -999.0000  -99.0000  -99.0000
 16  35  -999.0000  -999.0000  -99.0000  -99.0000
 17   0  -999.0000  -999.0000  -99.0000  -99.0000
 17   1  -999.0000  -999.0000  -99.0000  -99.0000
 17   2  -999.0000  -999.0000  -99.0000  -99.0000
 17   3  -999.0000  -999.0000  -99.0000  -99.0000
 17   4  -999.0000  -999.0000  -99.0000  -99.0000
 17   5  -999.0000  -999.0000  -99.0000  -99.0000
 17   6  -999.0000  -999.0000  -99.0000  -99.0000
 17   7  -999.0000  -999.0000  -99.0000  -99.0000
 17   8  -999.0000  -999.0000  -99.0000  -99.0000
 17   9  -999.0000  -999.0000  -99.0000  -99.0000
 17  10  -999.0000  -999.0000  -99.0000  -99.0000
 17  11  -999.0000  -999.0000  -99.0000  -99.0000
 17  12  -999.0000  -999.0000  -99.0000  -99.0000
 17  13  -999.0000  -999.0000  -99.0000  -99.0000
 17  14  -180.0000  -172.7151  -80.4083  -80.0000
 17  15  -180.0000  -115.1274  -83.6250  -80.0000
 17  16  -180.0000   -57.5397  -86.8167  -80.0000
 17  17  -180.0000    57.2957  -90.0000  -80.0000
 17  18    -0.0040   180.0000  -90.0000  -80.0000
 17  19    57.5877   180.0000  -86.8167  -80.0000
 17  20   115.1754   180.0000  -83.6250  -80.0000
 17  21   172.7631   180.0000  -80.4083  -80.0000
 17  22  -999.0000  -999.0000  -99.0000  -99.0000
 17  23  -999.0000  -999.0000  -99.0000  -99.0000
 17  24  -999.0000  -999.0000  -99.0000  -99.0000
 17  25  -999.0000  -999.0000  -99.0000  -99.0000
 17  26  -999.0000  -999.0000  -99.0000  -99.0000
 17  27  -999.0000  -999.0000  -99.0000  -99.0000
 17  28  -999.0000  -999.0000  -99.0000  -99.0000
 17  29  -999.0000  -999.0000  -99.0000  -99.0000
 17  30  -999.0000  -999.0000  -99.0000  -99.0000
 17  31  -999.0000  -999.0000  -99.0000  -99.0000
 17  32  -999.0000  -999.0000  -99.0000  -99.0000
 17  33  -999.0000  -999.0000  -99.0000  -99.0000
 17  34  -999.0000  -999.0000  -99.0000  -99.0000
 17  35  -999.0000  -999.0000  -99.0000  -99.0000
"""


def _load_coordinates():
    # TODO: This is slow, convert SINOSOIDAL_GRID_COORDINATES_STRING to a dict of lists
    coordinates_io = StringIO(SINOSOIDAL_GRID_COORDINATES_STRING)
    coordinates_df = pd.read_csv(coordinates_io, delimiter=r"\s+")
    return coordinates_df


def latlng_to_modis(lat_deg, lng_deg):
    """
    Convert latitude and longitude coordinates to `Modis Sinusoidal Grid
    <https://modis-land.gsfc.nasa.gov/MODLAND_grid.html>`_

    Args:
        lat_deg (float): latitude in degrees -90 to 90
        lng_deg (float): longitude in degrees -180 to 180

    Return:
        h (int): horizontal location on Modis grid
        v (int): vertical location on Modis grid
    """
    if not -90 <= lat_deg <= 90:
        raise ValueError('Latitude must be between -90 and 90 degrees')

    if not -180 <= lng_deg <= 180:
        raise ValueError('Longitude must be between -180 and 180 degrees')

    is_lng_in_bounds = (COORDINATES_TABLE['lon_min'] <= lng_deg) & (COORDINATES_TABLE['lon_max'] >= lng_deg)
    is_lat_in_bounds = (COORDINATES_TABLE['lat_min'] <= lat_deg) & (COORDINATES_TABLE['lat_max'] >= lat_deg)
    coordinates = COORDINATES_TABLE[is_lng_in_bounds & is_lat_in_bounds]

    # It is possible that a coordinate is present in upto four chips if both latitude and longitude are on the chip
    # boundary. It is not clear how Modis grid handles boundaries.
    # TODO: Update this method to return a list of coordinates, it is possible that a LatLng cooresponds to multiple
    # valid Modis coordinates.
    if len(coordinates) > 1:
        print('Warning: Only one of multiple Modis coordinates is being used'.format(lat_deg, lng_deg))

    return coordinates['iv'].iloc[0], coordinates['ih'].iloc[0]


COORDINATES_TABLE = _load_coordinates()