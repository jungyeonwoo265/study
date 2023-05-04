from sklearn import svm
xor_data = [[0,0,0],
            [0,1,1],
            [1,0,1],
            [1,1,0]]

data = []
labal = []
for row in xor_data:
    p = row[0]
    q = row[1]
    r = row[2]
    data.append([p, q])
    labal.append(r)

clf = svm.SVC()
clf.fit(data,labal)

pre = clf.predict(data)
print("예측결과: ", pre)

ok = 0; total = 0
for idx, answer in enumerate(labal):
    p = pre[idx]
    if p == answer:
        ok += 1
    total += 1
print("정답률: ", ok, "/", total, "=", ok/total)

