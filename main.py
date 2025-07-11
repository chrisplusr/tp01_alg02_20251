import os
import json
import sys
import subprocess

import utils
import filtrar_csv

if __name__ == '__main__':
    import os
    print(os.getcwd())
    url = "https://ckan.pbh.gov.br/dataset/ec3efaac-0ca6-4846-9e32-0ffff2d76dbb/resource/a35a0ed3-c933-4919-b23f-b925c37b64b8/download/20250401_atividade_economica.csv"
    filename = "data/20250401_atividade_economica.csv"
    
    # Garante que a pasta 'data' existe
    os.makedirs('data', exist_ok=True)
    
    if not os.path.exists(filename):
        utils.downloadFile(url, filename)
    else:
        print(f"[✓] O arquivo '{filename}' já existe. Nenhum download necessário.")

    filteredData = 'data/atividade_economica_filtrada.csv'
    if not os.path.exists(filteredData):
        filtrar_csv.main(filename, filteredData)
    else:
        print(f"[✓] O arquivo '{filteredData}' já existe. Nenhum processo necessário.")

    # 2) Salva em CSV separado
    coordinatesData = "data/cordenadas_bares_restaurantes.csv"
    if not os.path.exists(coordinatesData):
        coords  = utils.getCoordinates(filteredData)
        utils.saveCoordinatesToCsv(coords, coordinatesData)
    else:
        print(f"[✓] O arquivo '{coordinatesData}' já existe. Nenhum processo necessário.")

    coordinatesGeoJson = "data/bares_restaurantes.geojson"
    if not os.path.exists(coordinatesGeoJson):
        utils.buildGeojson(filteredData, coordinatesData, coordinatesGeoJson)
        print(f"[✓] Conversão para GeoJson feita com sucesso.")
    else:
        print(f"[✓] O arquivo '{coordinatesGeoJson}' já existe. Nenhum processo necessário.")
        
    print("\nPreparação de dados concluída. Iniciando a aplicação web...")
    
    try:
        python_executable = sys.executable
        subprocess.run([python_executable, 'app.py'], check=True)
    except FileNotFoundError:
        print(f"Erro: O executável do Python não foi encontrado.")
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro ao executar a aplicação 'app.py': {e}")
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário.")