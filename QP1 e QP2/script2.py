from csv import reader, writer
import csv
import subprocess
import pandas as pd
import re

field_names = ['evolutionary_commit', 'base',
               'left', 'right', 'parent', 'region_change_evolutionary_commit_before', 'region_change_evolutionary_commit_after', 'region_conflict_before', 'region_conflict_after']
field_names_conflitos = ['merge', 'left', 'right', 'text', 'qt_conflict']
field_names_infos_per_repository = [
    'merge', 'left', 'right', '', 'qt_conflict']
field_names_infos_per_repository_conflitc = [
    'merge', 'left', 'right', '', 'qt_conflict']
arrayWithDictionarys = []

qtSourceFile = []
arrayWithDictionarysConflicts = []
arquivos_conflitos_analisados = []
arquivos_conflitos_nao_analisados = []
qt_conflict_per_cenario = 0
qt_conflict_per_cenario_valido_js = 0

# csv por cenários
field_names_infos_per_cen_conflicts = ['merge', 'left', 'right', 'arquivos_conflitos_analisados', 'arquivos_conflitos_nao_analisados',
                                       'quantidade_total_de_conflitos_validos_js', 'quantidade_regioes_de_conflito_total',
                                       'quantidade_regioes_de_conflito_total_valido_js']
arquivos_conflitos_analisados_per_cen = []
arquivos_conflitos_nao_analisados_per_cen = []
quantidade_conflitos_validos_cen_merge = 0
arrayWithDictionarysPerCen = []
quantidade_cenarios_conflitos = 0
quantidade_conflitos_arquivos_validos_per_cen = 0
qtTotalConflitos = 0

# csv geral
field_names_infos_geral_conflicts = ['merge', 'left', 'right', 'arquivos_conflitos_analisados', 'arquivos_conflitos_nao_analisados',
                                       'quantidade_total_de_conflitos_validos_js',
                                       'quantidade_regioes_de_conflito_total', 'quantidade_regioes_de_conflito_total_valido_js']
quantidade_cenarios = 0
quantidade_conflitos = 0
quantidade_conflitos_arquivos_validos = 0
quantidade_regioes_de_conflito_total = 0
quantidade_regioes_de_conflitos_arquivos_validos = 0
arrayWithDictionarysGeral = []

def commit_pattern(commit):

    pattern = r"^\b[0-9a-f]{5,40}\b$"

    return bool(re.match(pattern, commit))


with open('conflicts.csv', 'r+', encoding="utf8", errors='ignore') as file_obj:

    # Create reader object by passing the file
    # object to reader method
    reader_obj = reader((line.replace('\0', '')
                        for line in file_obj), delimiter=",")
    writer_obj = writer(file_obj, quoting=csv.QUOTE_ALL)

    # Iterate over each row in the csv
    # file using reader object
    for row in reader_obj:

        quantidade_cenarios = quantidade_cenarios + 1

        subprocess.getstatusoutput('git checkout %s' % row[1])
        textMerge = subprocess.getoutput('git merge %s' % row[2])

        diff = subprocess.getoutput('git diff -U0')

        arrayDiff = diff.split()

        quantidade_cenarios_conflitos = quantidade_cenarios_conflitos + 1

        sourceConflict = []
        region_conflict = []
        id_conflict = 0
        cont_marcardor_arroba = 0

        # por cenário
        arquivos_conflitos_analisados_per_cen = []
        arquivos_conflitos_nao_analisados_per_cen = []
        quantidade_regioes_conflito_validos_cen_merge = 0
        quantidade_regioes_de_conflito_total_per_cen = 0
        quantidade_conflitos_arquivos_validos_per_cen = 0

        for index, str in enumerate(arrayDiff):

            # Salvando caminho do arquivo conflitante.
            if (str == "--cc"):
                id_conflict = id_conflict + 1
                sourceConflict.append(arrayDiff[index+1])

            # Salvando região de conflito do arquivo conflitante.
            if (str == '@@@'):
                cont_marcardor_arroba = cont_marcardor_arroba + 1
                if ((cont_marcardor_arroba % 2) != 0):
                    quantidade_regioes_de_conflito_total = quantidade_regioes_de_conflito_total + 1
                    quantidade_regioes_de_conflito_total_per_cen = quantidade_regioes_de_conflito_total_per_cen + 1
                    tupla_region = arrayDiff[index+1], arrayDiff[index +
                                                                 2], arrayDiff[index+3], id_conflict
                    region_conflict.append(tupla_region)

        for element in region_conflict:

            interval_colected = []

            # LEFT
            left = element[0]

            index_after_commom = 0

            # getting first interval
            first_interval_left = ''
            for index3, str in enumerate(left[1:]):

                if (str != ','):
                    first_interval_left = first_interval_left + str
                else:
                    index_after_commom = index3+2
                    first_interval_left_int = int(first_interval_left)
                    break

            # getting second interval
            second_interval_left = ''
            for str in left[index_after_commom:]:
                second_interval_left = second_interval_left + str

            second_interval_left_int = int(second_interval_left)
            tupla_interval_left = first_interval_left_int, second_interval_left_int

            interval_colected.append(tupla_interval_left)

            # RIGHT
            right = element[1]

            index_after_commom = 0

            # getting first interval
            first_interval_right = ''
            for index3, str in enumerate(right[1:]):

                if (str != ','):
                    first_interval_right = first_interval_right + str
                else:
                    index_after_commom = index3+2
                    first_interval_right_int = int(first_interval_right)
                    break

            # getting second interval
            second_interval_right = ''
            for str in right[index_after_commom:]:
                second_interval_right = second_interval_right + str

            second_interval_right_int = int(second_interval_right)
            tuple_interval_right = first_interval_right_int, second_interval_right_int

            interval_colected.append(tuple_interval_right)

            left_interval = interval_colected[0]
            right_interval = interval_colected[1]

            # getting evolutionary commits by interval
            indexSourceFile = element[-1] - 1
            source = sourceConflict[indexSourceFile]

            sourceArray = source.split('.')
            folderFile = sourceArray[0].split('/')
            folderFile = folderFile[0]

            if (sourceArray[-1] == 'js'):
                if (folderFile == 'test' or folderFile == 'spec' or sourceArray[-2] == 'test' 
                    or sourceArray[-2] == 'runtime' or folderFile == 'dist' or folderFile == 'build' or folderFile == 'packages'):
                    if (source not in arquivos_conflitos_nao_analisados_per_cen):
                        arquivos_conflitos_nao_analisados_per_cen.append(source)

                    if (source not in arquivos_conflitos_nao_analisados):
                        arquivos_conflitos_nao_analisados.append(source)

                    break

                quantidade_regioes_conflito_validos_cen_merge = quantidade_regioes_conflito_validos_cen_merge + 1
                quantidade_regioes_de_conflitos_arquivos_validos = quantidade_regioes_de_conflitos_arquivos_validos + 1

                if (source not in qtSourceFile):
                    qtSourceFile.append(source)

                if (source not in arquivos_conflitos_analisados):
                    arquivos_conflitos_analisados.append(source)

                if (source not in arquivos_conflitos_analisados_per_cen):
                    arquivos_conflitos_analisados_per_cen.append(source)

                # Pegando os commits evolucionários das regiões de conflito de arquivos válidos (LEFT)
                evolutionaryMessage = subprocess.getoutput('git log -L %d,%d:%s %s..%s' % (
                    left_interval[0], left_interval[0]+left_interval[1]-1, source, row[2], row[1]))
                evolutionaryMessageArrayLeft = evolutionaryMessage.split()
                arrayCommitsEvolutionaryLeft = []

                regionChangeBefore = []
                regionChangeAfter = []
                regionConflictBefore = []
                regionConflictAfter = []
                id_commit = 0

                if (len(evolutionaryMessageArrayLeft) != 0):
                    if (evolutionaryMessageArrayLeft[0] != 'fatal:'):
                        cont_marcardor_arroba_change = 0
                        region_change_evolutionary_commit = []

                        for index4, messageEvolutionary in enumerate(evolutionaryMessageArrayLeft):
                            if (messageEvolutionary == 'commit'):
                                hashCommit = index4 + 1
                                commit = evolutionaryMessageArrayLeft[hashCommit]
                                if (commit_pattern(commit)):
                                    if (evolutionaryMessageArrayLeft[index4 + 2] != 'Merge:'):
                                        arrayCommitsEvolutionaryLeft.append(
                                            evolutionaryMessageArrayLeft[hashCommit])

                            if (messageEvolutionary == "--git"):
                                regionConflictBefore.append(
                                    evolutionaryMessageArrayLeft[index4+1])
                                regionConflictAfter.append(
                                    evolutionaryMessageArrayLeft[index4+2])

                            if (messageEvolutionary == '@@'):

                                cont_marcardor_arroba_change = cont_marcardor_arroba_change + 1
                                if ((cont_marcardor_arroba_change % 2) != 0):
                                    regionChangeBefore.append(
                                        evolutionaryMessageArrayLeft[index4+1])
                                    regionChangeAfter.append(
                                        evolutionaryMessageArrayLeft[index4+2])

                        for index5, evolutionarycommit in enumerate(arrayCommitsEvolutionaryLeft):
                            my_dict_evolutionary_commit = {
                                'evolutionary_commit': '', 'base': '', 'left': '', 'right': ''}
                            my_dict_evolutionary_commit['evolutionary_commit'] = evolutionarycommit
                            my_dict_evolutionary_commit['base'] = row[0]
                            my_dict_evolutionary_commit['left'] = row[1]
                            my_dict_evolutionary_commit['right'] = row[2]
                            my_dict_evolutionary_commit['parent'] = 'left'
                            my_dict_evolutionary_commit['region_conflict_before'] = regionConflictBefore[index5]
                            my_dict_evolutionary_commit['region_conflict_after'] = regionConflictAfter[index5]
                            my_dict_evolutionary_commit['region_change_evolutionary_commit_before'] = regionChangeBefore[index5]
                            my_dict_evolutionary_commit['region_change_evolutionary_commit_after'] = regionChangeAfter[index5]
                            arrayWithDictionarys.append(
                                my_dict_evolutionary_commit)

                evolutionaryMessageRight = subprocess.getoutput('git log -L %d,%d:%s %s..%s' % (
                    right_interval[0], right_interval[0]+right_interval[1]-1, source, row[1], row[2]))
                evolutionaryMessageArrayRight = evolutionaryMessageRight.split()
                arrayCommitsEvolutionaryRight = []

                regionChangeBeforeRight = []
                regionChangeAfterRight = []
                regionConflictBeforeRight = []
                regionConflictAfterRight = []

                if (len(evolutionaryMessageArrayRight) != 0):
                    if (evolutionaryMessageArrayRight[0] != 'fatal:'):
                        cont_marcardor_arroba_change = 0
                        region_change_evolutionary_commit = []

                        for index5, messageEvolutionary in enumerate(evolutionaryMessageArrayRight):
                            if (messageEvolutionary == 'commit'):
                                hashCommit = index5 + 1
                                commit = evolutionaryMessageArrayRight[hashCommit]
                                if (commit_pattern(commit)):
                                    if (evolutionaryMessageArrayRight[index5 + 2] != 'Merge:'):
                                        arrayCommitsEvolutionaryRight.append(
                                            evolutionaryMessageArrayRight[hashCommit])

                            if (messageEvolutionary == "--git"):
                                regionConflictBeforeRight.append(
                                    evolutionaryMessageArrayRight[index5+1])
                                regionConflictAfterRight.append(
                                    evolutionaryMessageArrayRight[index5+2])

                            if (messageEvolutionary == '@@'):
                                cont_marcardor_arroba_change = cont_marcardor_arroba_change + 1
                                if ((cont_marcardor_arroba_change % 2) != 0):
                                    regionChangeBeforeRight.append(
                                        evolutionaryMessageArrayRight[index5+1])
                                    regionChangeAfterRight.append(
                                        evolutionaryMessageArrayRight[index5+2])

                        for index6, evolutionarycommit in enumerate(arrayCommitsEvolutionaryRight):

                            regionChangeBeforeRight[index6]
                            regionChangeAfterRight[index6]
                            my_dict_evolutionary_commit = {
                                'evolutionary_commit': '', 'base': '', 'left': '', 'right': ''}
                            my_dict_evolutionary_commit['evolutionary_commit'] = evolutionarycommit
                            my_dict_evolutionary_commit['base'] = row[0]
                            my_dict_evolutionary_commit['left'] = row[1]
                            my_dict_evolutionary_commit['right'] = row[2]
                            my_dict_evolutionary_commit['parent'] = 'right'

                            my_dict_evolutionary_commit['region_conflict_before'] = regionConflictBeforeRight[index6]
                            my_dict_evolutionary_commit['region_conflict_after'] = regionConflictAfterRight[index6]
                            my_dict_evolutionary_commit['region_change_evolutionary_commit_before'] = regionChangeBeforeRight[index6]
                            my_dict_evolutionary_commit['region_change_evolutionary_commit_after'] = regionChangeAfterRight[index6]
                            arrayWithDictionarys.append(
                                my_dict_evolutionary_commit)

                with open('evolutionary.csv', 'w') as csvfile:
                    writer = csv.DictWriter(
                        csvfile, fieldnames=field_names)
                    writer.writeheader()
                    writer.writerows(arrayWithDictionarys)
            else:
                if (source not in arquivos_conflitos_nao_analisados_per_cen):
                    arquivos_conflitos_nao_analisados_per_cen.append(source)

                if (source not in arquivos_conflitos_nao_analisados):
                    arquivos_conflitos_nao_analisados.append(source)

        quantidade_conflitos_arquivos_validos_per_cen = quantidade_conflitos_arquivos_validos_per_cen + \
            len(arquivos_conflitos_analisados_per_cen)

        my_dict_per_cen_conflict = {
            'merge': '', 'left': '', 'right': '', }
        my_dict_per_cen_conflict['merge'] = row[0]
        my_dict_per_cen_conflict['left'] = row[1]
        my_dict_per_cen_conflict['right'] = row[2]
        my_dict_per_cen_conflict['arquivos_conflitos_analisados'] = arquivos_conflitos_analisados_per_cen
        my_dict_per_cen_conflict['arquivos_conflitos_nao_analisados'] = arquivos_conflitos_nao_analisados_per_cen
        my_dict_per_cen_conflict['quantidade_total_de_conflitos_validos_js'] = quantidade_conflitos_arquivos_validos_per_cen
        my_dict_per_cen_conflict['quantidade_regioes_de_conflito_total'] = quantidade_regioes_de_conflito_total_per_cen
        my_dict_per_cen_conflict['quantidade_regioes_de_conflito_total_valido_js'] = quantidade_regioes_conflito_validos_cen_merge
        arrayWithDictionarysPerCen.append(
            my_dict_per_cen_conflict)
        
        qtTotalConflitos = qtTotalConflitos + quantidade_conflitos_arquivos_validos_per_cen

        with open('conflicts_per_cenario.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names_infos_per_cen_conflicts)
            writer.writeheader()
            writer.writerows(arrayWithDictionarysPerCen)

        subprocess.getstatusoutput('git reset --merge %s' % row[1])
    
    my_dict_geral_conflict = {
            'merge': '', 'left': '', 'right': '', }
    my_dict_geral_conflict['merge'] = row[0]
    my_dict_geral_conflict['left'] = row[1]
    my_dict_geral_conflict['right'] = row[2]
    my_dict_geral_conflict['arquivos_conflitos_analisados'] = arquivos_conflitos_analisados
    my_dict_geral_conflict['arquivos_conflitos_nao_analisados'] = arquivos_conflitos_nao_analisados
    my_dict_geral_conflict['quantidade_total_de_conflitos_validos_js'] = qtTotalConflitos
    my_dict_geral_conflict['quantidade_regioes_de_conflito_total'] = quantidade_regioes_de_conflito_total
    my_dict_geral_conflict['quantidade_regioes_de_conflito_total_valido_js'] = quantidade_regioes_de_conflitos_arquivos_validos
    arrayWithDictionarysGeral.append(
            my_dict_geral_conflict)
    
    with open('info_gerais_conflicts.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names_infos_geral_conflicts)
        writer.writeheader()
        writer.writerows(arrayWithDictionarysGeral)

print('quantidade de cenários com conflitos', quantidade_cenarios_conflitos)
print('quantidade total de conflitos em arquivos .js',
      qtTotalConflitos)
print('quantidade total de regiões de conflito',
      quantidade_regioes_de_conflito_total)
print('quantidade total de regiões de conflito em arquivos .js',
      quantidade_regioes_de_conflitos_arquivos_validos)
