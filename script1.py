from csv import reader, writer
import csv
import subprocess

field_names_conflitos = ['merge', 'left', 'right', 'text', 'qt_conflict']
arrayWithDictionarysConflicts = []
arquivos_conflitos_analisados = []
arquivos_conflitos_nao_analisados = []
qt_conflict_per_cenario = 0
qt_conflict_per_cenario_valido_js = 0
quantidade_cenarios = 0
quantidade_cenarios_conflitos = 0
quantidade_conflitos = 0

with open('arq.csv', 'r+', encoding="utf8", errors='ignore') as file_obj:

    # Create reader object by passing the file
    # object to reader method
    reader_obj = reader((line.replace('\0', '')
                        for line in file_obj), delimiter=",")
    writer_obj = writer(file_obj, quoting=csv.QUOTE_ALL)

    # Iterate over each row in the csv
    # file using reader object

    for row in reader_obj:
        qt_conflict_per_cenario = 0
        qt_conflict_per_cenario_valido_js = 0

        my_dict_evolutionary_commit = {
            'merge': '', 'left': '', 'right': '', 'text': ''}
        print('~~~~ AQUI COMEÇA O MERGE ~~~~~')
        quantidade_cenarios = quantidade_cenarios + 1
        qtSourceFile = []

        subprocess.getstatusoutput('git checkout %s' % row[1])
        textMerge = subprocess.getoutput('git merge %s' % row[2])
        arrayTextMerge = textMerge.split()

        for index, text in enumerate(arrayTextMerge):
            if (text == "CONFLITO" or text == "CONFLICT"):
                qt_conflict_per_cenario = qt_conflict_per_cenario + 1
                quantidade_conflitos = quantidade_conflitos + 1

        diff = subprocess.getoutput('git diff -U0')

        arrayDiff = diff.split()

        if (len(arrayDiff) != 0):
            print('ESSE TEM CONFLITO')
            quantidade_cenarios_conflitos = quantidade_cenarios_conflitos + 1

            my_dict_evolutionary_commit['merge'] = row[0]
            my_dict_evolutionary_commit['left'] = row[1]
            my_dict_evolutionary_commit['right'] = row[2]
            my_dict_evolutionary_commit['text'] = arrayTextMerge
            my_dict_evolutionary_commit['qt_conflict'] = qt_conflict_per_cenario

            arrayWithDictionarysConflicts.append(
                my_dict_evolutionary_commit)

            with open('conflicts.csv', 'w') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=field_names_conflitos)
                writer.writeheader()
                writer.writerows(arrayWithDictionarysConflicts)
        
        subprocess.getstatusoutput('git reset --merge %s' % row[1])
