def work():
    total = len(a)
    done = 0
    for i in a:
        print(f"DONE:{done}\nTOTAL:{total}")
        done += 1
        name = i.moviedisplay
        if any("tunestream" in str(x).lower() for x in (i.url, i.alt1, i.alt2)):
            print(f"skipping {name}")
            continue
        print(f"adding {name}")
        data = main_(name, only_return_result=True)
        if not data:
            continue
        print("Recieved Data:", data[0], data[1], data[2], data[3], data[4])
        i.name = data[0]
        i.url = data[1]
        i.alt1 = data[2]
        i.alt2 = data[3]
        if not i.subs:
            i.subs = data[5]
        print("updating")
        db.session.commit()


#         
#         
#         
