# coding: UTF-8
#from https://github.com/NlGG/matching
def deferred_acceptance(m_prefs, f_prefs,caps=None):
    mnum = len(m_prefs) #さらにmnumをunmatchedにも対応させている
    single=range(mnum)  #最初はみんな独身
    fnum = len(f_prefs)
    married = {}
    have = [mnum for i in range(fnum)]#最初は皆受け入れるので、付き合っている人は最も序列の低いunmatchedとしてのmnumで統一して全部入れる
    down = [0 for i in range(mnum)]#０で全部入れる。



    while len(single) > 0:

        for i in single:

            mbest = m_prefs[i][down[i]]#アプローチされた女性

            if mbest != fnum:# アプローチされた女性が実態のある人なら

                if f_prefs[mbest].index(i) < f_prefs[mbest].index(have[mbest]): #aList = [123, 'xyz', 'zara', 'abc']で 　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　aList.index( 'xyz' ) は１、aList.index( 'zara' ) は２が返される。                     #iが、アプローチされた女性の選好において何番目に位置するか＜すでに付き合っている男性（最初はunmatched)が、プローチされた女性の選好において何番目に位置するか
                    single.remove(i)#仮として結ばれ独身でなくなる
                    if have[mbest] != mnum: #すでに付き合っている男性がunmatchedでなく、普通の男性なら、
                        single.append(have[mbest]) #その男性は独身になる
                    have[mbest] = i                #代わってiさんが仮の付き合ってる人になる
                else: #iが、アプローチされた女性の選好において何番目に位置するか＞すでに付き合っている男性が、プローチされた女性の選好において何番目に位置するか　で恋に敗れてしまったら
                    if down[i] < fnum - 1: #まだ希望があれば
                        down[i] += 1#選好を一つ落としてまた頑張ろう
                    else:#もう選択肢がなければ、
                        single.remove(i)#戦闘から離脱して大人しく、i: fnumってことにしろ
                        married.update({i: fnum})
            else:#もうunmatchedだったら、そこで終わり。戦闘から離脱して大人しく、i: fnumってことにしろ
                single.remove(i)
                married.update({i: fnum})

    for i in have:
        if i != mnum:
            married.update({i: have.index(i)})

    married = married.items()#The method items() returns a list of dict's (key, value) tuple pairs
                             #例えば、dict = {'Name': 'Zara', 'Age': 7}で、dict.items()とすると[('Age', 7), ('Name', 'Zara')]と返す
    m_matched_computed = []
    for i in range(mnum):
        m_matched_computed.append(married[i][1])
    f_matched_computed = have
    
    return m_matched_computed, f_matched_computed
