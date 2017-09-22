-- book : programming Haskell chapter 5 
module Chap5  where
  
import Data.Char


  
  
-- lecture

lowers = length.filter isLower

counter x= length. filter (x==)

rotate n xs = drop n xs ++ take n xs

factors n = [x | x<-[1..n], n`mod`x==0]

find k t = [v | (k', v) <- t, k==k']

safe_div :: Float -> Float -> Float
safe_div _ 0 = 0
safe_div n m = n / m

positions x xs = [i | (i, x') <- zip [0..] xs, x==x']

let2int :: Char -> Int
let2int c = ord c - ord 'a'

int2let :: Int -> Char
int2let n = chr (ord 'a' + n)


shift :: Int -> Char -> Char
shift n c | isLower c = int2let ((let2int c + n) `mod` 26)
          | otherwise = c

encode :: Int -> String -> String
encode n = map (shift n)
          
percent :: Int -> Int -> Float
percent n m = (fromIntegral n `safe_div` fromIntegral m) * 100

freqs :: String -> [Float]
freqs xs = [percent (counter x xs) n | x <- ['a'..'z']]
  where n = lowers xs

chisqr :: [Float] -> [Float] -> Float
chisqr os es = sum [((o-e)^2)`safe_div`e | (o, e) <- zip os es]


crack :: String -> String
crack xs = encode (-factor) xs
  where factor = head (positions (minimum chitab) chitab)
        chitab = [chisqr (rotate n table') table | n <- [0..25]]
        table' = freqs xs


table = freqs test_str
  

-- exercise

pyths maxnum = [(x,y,z)| x <- [1..maxnum], y<- [1..maxnum], z<-[1..maxnum], z^2==x^2+y^2]

perfect maxnum = [x | x <- [1..maxnum], x == (sum$init$factors x)]
  --filter (\x -> (==) x $ sum $ init $ factors x)  [1..maxnum]

positions_ x xs = [i | i <- find x (zip xs [0..])]

scalar_product xs ys =  sum [x*y | (x,y) <- zip xs ys]
  
-- database

test_str = "that was first spoken in early medieval England and is now the global lingua franca.[4][5] Named after the Angles, one of the Germanic tribes that migrated to England, it ultimately derives its name from the Anglia (Angeln) peninsula in the Baltic Sea. It is closely related to the Frisian languages, but its vocabulary has been significantly influenced by other Germanic languages, as well as by Latin and Romance languages, particularly French.[6]English has developed over the course of more than 1,400 years. The earliest forms of English, a set of Anglo-Frisian dialects brought to Great Britain by Anglo-Saxon settlers in the 5th century, are called Old English. Middle English began in the late 11th century with the Norman conquest of England, and was a period in which the language was influenced by French.[7] Early Modern English began in the late 15th century with the introduction of the printing press to London and the King James Bible, and the start of the Great Vowel Shift.[8] Through the worldwide influence of the British Empire, modern English spread around the world from the 17th to mid-20th centuries. Through all types of printed and electronic media, as well as the emergence of the United States as a global superpower, English has become the leading language of international discourse and the lingua franca in many regions and in professional contexts such as science, navigation, and law.[9]English is either the official language or one of the official languages in almost 60 sovereign states. It is the most commonly spoken language in the United Kingdom, the United States, Canada, Australia, Ireland, and New Zealand, and is widely spoken in some areas of the Caribbean, Africa, and South Asia.[10] It is the third most common native language in the world, after Mandarin and Spanish.[11] It is the most widely learned second language and an official language of the United Nations, of the European Union, and of many other world and regional international organisations. It is the most widely spoken Germanic language, accounting for at least 70% of speakers of this Indo-European branchModern English grammar is the result of a gradual change from a typical Indo-European dependent marking pattern with a rich inflectional morphology and relatively free word order, to a mostly analytic pattern with little inflection, a fairly fixed SVO word order and a complex syntax.[12] Modern English relies more on auxiliary verbs and word order for the expression of complex tenses, aspect and mood, as well as passive constructions, interrogatives and some negation. Despite noticeable variation among the accents and dialects of English used in different countries and regions – in terms of phonetics and phonology, and sometimes also vocabulary, grammar and spelling – English-speakers from around the world are able to communicate with one another with relative ease."
