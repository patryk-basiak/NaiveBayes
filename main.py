flowerList = []
data_label = []
with open('iris_training.txt', 'r') as file:
    for line in file:
        data_line = line.strip().replace(",", ".").split()
        if data_line[-1] not in data_label:
            data_label.append(data_line[-1])
        flowerList.append(data_line)
testList = []
with open('iris_test.txt', 'r') as file:
    for line in file:
        testList.append(line.strip().replace(",", ".").split())

def transform_data(training_data):
    data = {}
    for x in training_data:
        if x[-1] not in data:
            data[x[-1]] = [{} for _ in range(len(x)-1)]
        for i in range(len(x)-1):
            if not x[i] in data[x[-1]][i]:
                data[x[-1]][i][x[i]] = 0
            data[x[-1]][i][x[i]] += 1
    return data

transformed_Data = transform_data(flowerList)
def count_columns(training_data):
    for label in training_data:
        for x in training_data[label]:
            s = 0
            for f in flowerList:
                if f[-1] == label:
                    s +=1
            for y in x:
                x[y] = x[y]/s
    return training_data

counted_data = count_columns(transformed_Data)
def test(test_list, train_list):
    correct = 0
    result_pair = []
    for x in test_list:
        decision_label = manual_test(x, train_list)
        if decision_label== x[-1]:
            correct+=1
        result_pair.append([x[-1], decision_label])
    print(f"Accuracy {correct}/{len(test_list)} which is {correct/ len(test_list)*100}%")
    return result_pair

def manual_test(prompt, train):
    mval = {}
    for label, data in train.items():
        suma = 1.0
        co = []
        flat = True
        length = 0
        for i, xd in enumerate(data):
            length= len(xd.keys())
            try:
                prop = float(xd[prompt[i]])
            except KeyError:
                flat = False
                print("Before smoothing:", 0)
                prop = 1 / (40 + len(xd.keys()))
                print("After smoothing:", prop)
            co.append(prop)

        if flat:
            print("Before smoothing:", co)
            co[0] = co[0] + 1/ (40 + length)
            print("After smoothing:", co)
        for c in co:
            suma *= c
        mval[label] = suma
    decision_label = max(mval, key=mval.get)
    return decision_label


result = test(testList, counted_data)
for k in range(4):
    for l in range(4):
        if k == 0 and l == 0:
            print("Correct\\Result", end="\t\t")
        elif k == 0 and l < 4:
            print(data_label[l-1], end="\t\t")
        elif l == 0 and k < 4:
            print(data_label[k-1], end="\t\t")
        else:
            print(result.count([data_label[k-1], data_label[l-1]]), end="\t\t")
    print()

def user_input(mess):
    mess = mess.replace(",", ".").split()
    try:
        for a in mess:
            float(a)
    except ValueError:
        print("Provide numbers")
        return
    if len(mess) != len(flowerList[0]) - 1:
        print("Wrong number of arguments")
        return
    print(manual_test(mess, counted_data))

while True:
    test = input("Write your points (seperated with white spaces): ")
    user_input(test)