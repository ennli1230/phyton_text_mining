import json
import pprint

pp = pprint.PrettyPrinter(indent=4)

dosya = open("ekonomi_0.json",encoding="utf8")
veri = json.load(dosya)
dosya.close()

dokumanlar = []

for haber in veri['List']:
    dokumanlar.append(haber['Title'].strip()+" "+haber['Description'].strip()+" "+haber['Text'].strip())
    
islenmis_dokumanlar = []

alfabe = "abcçdefgğhıijklmnoöpqrsştuüvwxyz "
alfabe_liste = list(alfabe)

for dokuman in dokumanlar:
    # Küçük harfe çevirelim...
    dokuman = dokuman.lower()
    
    # alfabede olmayan harfleri çıkartalım...
    dokuman_liste = list(dokuman)
    
    yeni_dokuman = []
    
    for harf in dokuman_liste:
        if harf in alfabe_liste:
            yeni_dokuman.append(harf)
            
    yeni_dokuman_string = "".join(yeni_dokuman)
    
    
    # işlenmiş dokümanlara ekleyelim...
    islenmis_dokumanlar.append(yeni_dokuman_string)
    
ilk_asama = []

for docid, dokuman in enumerate(islenmis_dokumanlar):
    
    kelimeler = dokuman.split(" ")
    
    for kelime in kelimeler:
        
        if len(kelime)==0:
            continue
        
        eklenecek_tuple = (kelime, docid)
        
        ilk_asama.append(eklenecek_tuple)
    
pp.pprint(ilk_asama[:1000])

ilk_asama.sort()

pp.pprint(ilk_asama[:1000])

son_kelime = ""

inverted_index = []

for kelime, docid in ilk_asama:
    
    if kelime != son_kelime:
        son_kelime = kelime
        eklenecek_tuple = (kelime, 1, [docid])
        inverted_index.append(eklenecek_tuple)
    else:
        kelime, frekans, postings = inverted_index[-1]
        
        if docid not in postings:
            postings.append(docid)
            frekans += 1
            
            yeni_tuple = (kelime, frekans, postings)
            
            inverted_index[-1] = yeni_tuple

pp.pprint(inverted_index[:1000])

permuterm_index = []

for word, freq, posting in inverted_index:
    ozel_karakter = '$'
    
    k1 = word+ozel_karakter
    
    permuterm_index.append((k1, word))
    
    for i in range(len(word)):
        k1 = k1[-1] + k1[0:len(word)]
        permuterm_index.append((k1, word))
        
        
liste1 = set()


for permuterm, word in permuterm_index:
    if permuterm.startswith('$adalet'):
        # postinglere ulaşalım
        for kelime, frekans, posting in inverted_index:
            if kelime == word:
                postingkumesi = set(posting)
                liste1 = liste1.union(postingkumesi)
                
print(liste1)


liste2 = set()


for permuterm, word in permuterm_index:
    if permuterm.startswith('$amerika'):
        # postinglere ulaşalım
        for kelime, frekans, posting in inverted_index:
            if kelime == word:
                postingkumesi = set(posting)
                liste2 = liste2.union(postingkumesi)
                
print(liste2)


sonuc = list(liste1.intersection(liste2))

sonuc.sort()
sonuc




