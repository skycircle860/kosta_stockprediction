#! /usr/bin/Rscript

#library(readr)
library(rJava)
library(rvest)
library(KoNLP)
library(stringr)

positive <- readLines(file("/root/SNS_Crawling/pos_pol_word.txt", encoding = "UTF-8"))
positive=positive[-1:-18]

negative <- readLines(file("/root/SNS_Crawling/neg_pol_word.txt", encoding = "UTF-8"))
negative=negative[-1:-18]


#검색 기업명 txt에서 불러오기
corporation <- readLines(file("/root/SNS_Crawling/corporation.txt", encoding = "UTF-8"))
print(corporation)

corporation_url <- paste0("/root/SNS_Crawling/deduplication/",corporation,"_dedupl.txt")
#print(corporation_url)

#형태소로 쪼개기
txt <- readLines(file(corporation_url, encoding = "euc-kr"))
#print(txt)

pos=SimplePos22(txt)
pos.vec=unlist(pos)

pos.vec<-gsub("[^가-힣]","",pos.vec) # 한글이 아닌것 삭제
pos.vec<-pos.vec[-c(which(pos.vec=="" | pos.vec=="#"))]

#print(pos.vec)

write.csv(pos.vec, paste0("/root/SNS_Crawling/KoNLP/",corporation,"_KoNLP.csv"), fileEncoding = "UTF-8")
pos.matches.num<-match(pos.vec,positive) # 긍정어 벡터 번호
neg.matches.num<-match(pos.vec,negative) # 부정어 벡터 번호

#pos.matches.num ; neg.matches.num

pos.matches <- !is.na(pos.matches.num)
neg.matches <- !is.na(neg.matches.num)

pos.sum=sum(pos.matches)
neg.sum=sum(neg.matches)
#pos.matches
#neg.matches
#pos.sum ; neg.sum

result <- pos.sum-neg.sum
result

if(result>0){
  res <- paste0("긍정적입니다 (",result,")")
}else if(result==0){
  res <- "데이터가 충분하지 않습니다."
}else{
  res <- paste0("부정적입니다 (",result,")")
}

write.csv(res,"/root/SNS_Crawling/result.csv",fileEncoding = "UTF-8")
