
with open("spec.csv", "r", encoding="utf-8") as fp:
    lines = fp.readlines()
    print(len(lines))

uniq = set()

for l in lines:
    uniq.add(l)

print(len(uniq)) 

with open("spec_uniq.csv", "w", encoding="utf-8") as fp:
    for l in uniq:
        fp.write(l)  