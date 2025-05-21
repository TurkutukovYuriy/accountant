import random
import time
#Библиотека для работы с расширением yaml
import yaml
#Библиотека для изменения цвета сообщений в консоли
from colorama import init, Fore
init()
#Класс настраиваемых исключений (заглушка для корректной обработки некоторых вводов)
class CustomException(Exception):
    def __str__(self):
        print()
#Основной класс
class Calculator:
#Методы
    #Конструктор
    #Передаем в конструктор списки: имен переменных, типов, допустимых диапазонов значений, значений по умолчанию +константу штрафа
    def __init__(self, arguments_names, arguments_types, arguments_values_range, arguments_default_values, FINE):
        self.arguments_names=arguments_names
        self.arguments_types=arguments_types
        self.arguments_values_range=arguments_values_range
        self.arguments_default_values=arguments_default_values
        self.FINE=FINE
    #Считаем количество переменных, которые будем использовать
        self.arguments_quantity=len(self.arguments_names)
    #Список текстовых подсказок для режимов
        self.text_mods = \
        [
            "select the calculator mode (enter 1 to choose preset creation mode, enter 2 to choose create mode, enter 3 to choose synergy mod): \n>>>",
            "select the name of the new preset: \n>>>",
            "select a calculation method (enter 1 for manual entry, enter 2 for use preset, enter to return to mode selection): \n>>>"
        ]
    #Список подсказок для переменных
        self.text_prompts = []
    #Создаем подсказки для переменных
        for i in range(self.arguments_quantity):
            self.text_prompts.append("Select "+self.arguments_names[i]+":"+" min value="+str(self.arguments_values_range[i][0])+", max value= "+str(self.arguments_values_range[i][1])+": \n>>>")
    #Список ошибок ввода
        self.text_errors=[]
    #Создаем текс ошибок
        for i in range(self.arguments_quantity):
            self.text_errors.append("The "+self.arguments_names[i]+" must be "+self.arguments_types[i]+" in the specified range!")
    # Колличество попыток ввода
        self.input_attempts=3
    #Список мемов, если закончились попытки ввода
        self.text_memes=\
            [
                "No signs of intelligence were found, ",
                "Your IQ is not very high, ",
                "You have 47 chromosomes, ",
                "Are you skibidy toilet?, "
            ]
    #Список текстовых последствий
        self.text_effects=\
            [
                "the preset has not been created!",
                "the mode was not changed!",
                "no operating mode with this index was found!",
                "the step was skipped,",
                "preset created!",
                "\nTHE PROGRAM HAS BEEN FORCED TO STOPPED!",
                "no calculation method with this index was found!",
                "manual input will be used!",
                "values will be used!",
                "the calculation method was not changed!",
                "the value from the preset was used!",
                "manual input failed!",
                "enter the name of the preset, you want to use:",
                "default value will be used!",
                "preset with this name not found!",
                "preset was not changed!"
             ]
    #Отключает некоторые процессы, при повторном вызове main_toggle
        self.print=True
    #Список приколов (в разработке)
        self.jokes_list=["the devil's conscience","laughter of emptiness","machine tears","dry water","essence of life","pyrolite","stardust"]
    #Список пресетов
        self.presets_list=[]

    #Вспомогательный метод чтения пресетов, принимает имя yaml файла как аргумент
    def reading_presets(self, file_name='presets.yaml'):
        # Список пресетов
        presets_list=[]
        # Подгружаем файл
        with open(file_name, "r") as fr:
            presets_dump = yaml.load(fr, Loader=yaml.FullLoader)
        # Распаковка
        for i in range(0, len(presets_dump)):
            presets_list.append(presets_dump[i])
        self.presets_list=presets_list


    #Вспомогательный метод записи пресетов, принимает имя yaml файла как аргумент
    def recording_presets(self, file_name='presets.yaml'):
        self.reading_presets()
        print(Fore.BLUE + "PRESET MODE ON: " + Fore.RESET + self.text_mods[1],end="")
        new_preset_name=input()
        # Создаем локальную копию списка пресетов
        copy_of_presets_list = self.presets_list
        #Создаем пресет
        new_preset=[]
        for i in range(self.arguments_quantity):

            for j in range(self.input_attempts):
                try:
                    # Локальная переменная ввода, позволяет корректно обрабатывать значения, вне зависимости от типа данных
                    value_str = input(self.text_prompts[i])

                    if value_str == "":
                        raise CustomException

                    elif self.arguments_types[i] == "int":
                        new_preset.append(int(value_str))

                    else:
                        new_preset.append(float(value_str))

                    if new_preset[i] >= self.arguments_values_range[i][0] and new_preset[i] <= self.arguments_values_range[i][1]:
                        break
                    else:
                        raise ValueError

                except CustomException:
                    print(Fore.YELLOW + "ATTENTION, " + self.text_effects[3] + Fore.RESET)
                    new_preset.append(self.arguments_default_values[i])
                    break

                except ValueError:
                    print(Fore.RED + self.text_errors[i] + Fore.RESET)
                    time.sleep(1)

            if new_preset[i] < self.arguments_values_range[i][0] or new_preset[i] > self.arguments_values_range[i][1]:
                print(
                    self.text_memes[random.randint(0, len(self.text_memes) - 1)] + Fore.RED + self.text_effects[0] + Fore.RESET)
                self.main_toggle()
        self.presets_list.append({new_preset_name: new_preset})

        with open(file_name, "w") as fw:
            yaml.dump(self.presets_list, fw)

        print(Fore.GREEN + "CONGRATULATIONS, " + self.text_effects[4] + Fore.RESET)
        self.main_toggle()


    #Вспомогательный метод расчета затрат при создании, принимает способ расчета, как аргумент
    def calculate_creation(self, method=2):
        #Определяем способ расчета
        if method == 1:
            print(Fore.YELLOW + "ATTENTION, " + self.text_effects[7] + Fore.RESET)
        #Создаем одноразовый пресет
            disposable_set=[]
            for i in range(self.arguments_quantity):
                for j in range(self.input_attempts):
                    try:
                        value_str = input(self.text_prompts[i])

                        if value_str == "":
                            raise CustomException

                        elif self.arguments_types[i] == "int":
                            disposable_set.append(int(value_str))

                        else:
                            disposable_set.append(float(value_str))

                        if disposable_set[i] >= self.arguments_values_range[i][0] and disposable_set[i] <= \
                                self.arguments_values_range[i][1]:
                            break

                        else:
                            raise ValueError

                    except CustomException:
                        time.sleep(0.1)
                        print(Fore.YELLOW + "ATTENTION, " + self.text_effects[10] + Fore.RESET)
                        disposable_set.append(self.arguments_default_values[i])
                        break

                    except ValueError:
                        print(Fore.RED + self.text_errors[i] + Fore.RESET)
                        time.sleep(1)

                if disposable_set[i] < self.arguments_values_range[i][0] or disposable_set[i] > \
                        self.arguments_values_range[i][1]:
                    print(self.text_memes[random.randint(0, len(self.text_memes) - 1)] + Fore.RED + self.text_effects[
                        11] + Fore.RESET)
                    self.main_toggle()

        # Генерация кубов
            # Локальный список для результатов бросков d4
            d4_list = []
            # Бросаем кубы
            for i in range(disposable_set[0]):
                d4_list.append(random.randint(1, 4))
            # Отдельно запишем сумму
            d4_list_sum = sum(d4_list)

            # Определяем значение штрафа и редкость предмета
            if disposable_set[0] == 4:
                fine = self.FINE
                item_rare = "homebrew"
            elif disposable_set[0] == 3:
                fine = 1
                item_rare = "rare"
            elif disposable_set[0] == 2:
                fine = 1
                item_rare = "unusual"
            elif disposable_set[0] == 1:
                fine = 1
                item_rare = "usual"

            # Считаем итоговый результат
            total_time = fine * (d4_list_sum - disposable_set[3])
            total_cost = disposable_set[1] * disposable_set[2]

            # Выводим подробную информацию
            print(Fore.GREEN + "CALCULATION COMPLETED!" + Fore.RESET)
            print(Fore.GREEN + "Created: " + "1" + " " + item_rare + " item(s)" + Fore.RESET)
            print("d4 role results: " + str(d4_list))
            print("total time = " + str(int(total_time))+" hours")
            print("total cost = " + str(int(total_cost))+" gold coins")

            if fine == self.FINE:
                print("In addition, bring Martin "+self.jokes_list[random.randint(0,len(self.jokes_list))]+" or some other joke")
                self.main_toggle()

            #Выходим
            self.main_toggle()

        if method==2:
            #Подметод расчета, принимает пресет как аргумент
            def calculate(preset):
                for i in range(0, len(preset)):
                    if self.arguments_types[i]=='int':
                        preset[i]=int(preset[i])
                    elif self.arguments_types[i]=='float':
                        preset[i]=float(preset[i])
                    else:
                        preset[i] = str(preset[i])

                print(Fore.YELLOW + "ATTENTION, this " +str(preset)+" "+self.text_effects[8] + Fore.RESET)
                #Генерация кубов
                #Локальный список для результатов бросков d4
                d4_list = []
                # Бросаем кубы
                for i in range((preset[0])):
                    d4_list.append(random.randint(1, 4))
                # Отдельно запишем сумму
                d4_list_sum = sum(d4_list)
                # Определяем значение штрафа и редкость предмета
                if preset[0] == 4:
                    fine = self.FINE
                    item_rare = "homebrew"
                elif preset[0] == 3:
                    fine = 1
                    item_rare = "rare"
                elif preset[0] == 2:
                    fine = 1
                    item_rare = "unusual"
                elif preset[0] == 1:
                    fine = 1
                    item_rare = "usual"

                # Считаем итоговый результат
                total_time = fine * (d4_list_sum - preset[3])
                total_cost = preset[1] * preset[2]

                # Выводим подробную информацию
                print(Fore.GREEN + "CALCULATION COMPLETED!" + Fore.RESET)
                print(Fore.GREEN + "Created: " + "1" + " " + item_rare + " item(s)" + Fore.RESET)
                print("d4 role results: " + str(d4_list))
                print("total time = " + str(int(total_time))+" hours")
                print("total cost = " + str(int(total_cost))+" gold coins")

                if fine == self.FINE:
                    print("In addition, bring Martin "+self.jokes_list[random.randint(0,len(self.jokes_list))]+" or some other joke")
                # Чистим за собой список
                d4_list.clear()
                #Выходим
                self.main_toggle()

            for i in range(self.input_attempts):
                #Получаем имя пресета
                preset_name = input(Fore.BLUE + "CREATION MODE, M2 ON: " + Fore.RESET + self.text_effects[12] + "\n>>>")
                #Ищем пресет
                for i in range(len(self.presets_list)):
                    try:
                        preset=self.presets_list[i][preset_name]
                        calculate(preset)
                    except:
                        time.sleep(1)
                print(self.text_memes[random.randint(0, len(self.text_memes)) - 1] + Fore.RED + self.text_effects[14] + Fore.RESET)

            print(self.text_memes[random.randint(0, len(self.text_memes))-1] + Fore.RED + self.text_effects[15] + Fore.RESET)
            self.main_toggle()







#Главный метод, отвечает за выбор режима работы калькулятора
    def main_toggle(self, mode=0):
        #Читаем пресеты
        self.reading_presets()
        if self.print==True:
            print(Fore.BLUE+"Workshop cost calculator by Ajax, v0.2"+Fore.RESET)
            self.print=False











        try:
            while True:

            #Режим выбора режима
                if mode==0:
                    for i in range(self.input_attempts):
                        try:
                            mode = int(input(Fore.BLUE+"SELECT MODE ON: "+Fore.RESET+self.text_mods[0]))
                            if mode <=3 and mode >=1:
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print(self.text_memes[random.randint(0,len(self.text_memes)-1)]+Fore.RED+self.text_effects[2]+Fore.RESET)
                            time.sleep(1)
                    if mode >3 or mode <1:
                        print(self.text_memes[random.randint(0, len(self.text_memes)-1)]+Fore.RED+self.text_effects[1]+Fore.RESET)
                        self.main_toggle()

            #Режим создания пресета
                elif mode==1:
                    self.recording_presets()

            #Режим расчета затрат на создание
                elif mode==2:
                    print(Fore.BLUE + "CREATION MODE ON: " + Fore.RESET + self.text_mods[2], end="")
                    for i in range(self.input_attempts):
                        try:
                            value_str=input()
                            if value_str=="":
                                raise CustomException
                            else:
                                method=int(value_str)
                            if method==1:
                                self.calculate_creation(1)
                            elif method==2:
                                self.calculate_creation(2)
                            else:
                                raise ValueError

                        except CustomException:
                            self.calculate_creation()
                        except ValueError:
                            print(self.text_memes[random.randint(0, len(self.text_memes) - 1)] + Fore.RED + self.text_effects[6] + Fore.RESET)
                            time.sleep(1)



                    print(self.text_memes[random.randint(0, len(self.text_memes))] + Fore.RED + self.text_effects[9] + Fore.RESET)
                    self.main_toggle()

                else:
                    print(Fore.YELLOW+"The mode does not exist or is under development!"+Fore.RESET)
                    self.main_toggle()




        #Внимание, откючает ВСЕ СИСТЕМНЫЕ сообщения об ошибках!
        # except:
        #     print()

        #Меняет сообщение о ручной остановке программы
        except KeyboardInterrupt:
            print(Fore.RED+self.text_effects[5]+Fore.RESET)
            exit(0)

#Функция чтения настроек, принимает имя файла, как аргумент, запускает калькулятор
def main_settings_unpack(file_name='settings.yaml'):
    #Списки настроек (их принимает конструктор калькулятора и они не изменяются по ходу работы программы)
    arguments_names=[]
    arguments_types=[]
    arguments_values_range=[]
    arguments_default_values=[]
    #Подгружаем файл
    with open(file_name) as file:
         settings_dump=yaml.load(file, Loader=yaml.FullLoader)
    #Нужный блок
    block=settings_dump["Arguments"]
    #Символы с пометкой на удаление
    remove_letter=["dict_keys","[","]","(",")","dict_values","'"]
    #Распаковка
    for i in range(0, len(block)-1):
        arguments_names.append(block[i].keys())
        for j in range(0, len(remove_letter)):
            arguments_names[i]=str(arguments_names[i]).replace(remove_letter[j], "")

    for i in range(0, len(block)-1):
        arguments_types.append(block[i][arguments_names[i]][0])
        arguments_values_range.append(block[i][arguments_names[i]][1])
        arguments_default_values.append(block[i][arguments_names[i]][2])
    #Отдельно достаем константу штрафа
    FINE=(block[-1]["fine"])
    #Создаем объект калькулятора
    cal=Calculator(arguments_names, arguments_types, arguments_values_range, arguments_default_values, FINE)
    #Вызываем
    cal.main_toggle()


main_settings_unpack()






























