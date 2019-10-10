library(rJava)
library(rvest)
library(KoNLP)
library(stringr)

positive <- readLines(file("/root/SNS_Crawling/pos_pol_word.txt", encoding = "UTF-8"))
positive=positive[-1:-18]

negative <- readLines(file("/root/SNS_Crawling/neg_pol_word.txt", encoding = "UTF-8"))
negative=negative[-1:-18]

txt <- readLines(file("/root/SNS_Crawling/deduplication/CJ대한통운_dedupl.txt",encoding = "euc-kr"))

pos=SimplePos22(txt)

pos.vec=unlist(pos)

pos.vec<-gsub("[^가-힣]","",pos.vec) # 한글이 아닌것 삭제

pos.vec<-pos.vec[-c(which(pos.vec=="" | pos.vec=="#"))]

write.csv(pos.vec,"/root/SNS_Crawling/KoNLP/CJ대한통운_KoNLP.csv",fileEncoding = "euc-kr")

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
#result

if(result>0){
  a <- "긍정"
  b <-as.data.frame(a,encoding="EUC-KR")
  write.csv(b,file = "/root/SNS_Crawling/KoNLP/KoNLP_Result.csv",append=FALSE, fileEncoding="euc-kr")
  print("긍정")
}else if(result==0){
  a <- "중립"
  b <- as.data.frame(a)
  write.csv(b,file = "/root/SNS_Crawling/KoNLP/KoNLP_Result.csv",append=FALSE, fileEncoding="euc-kr")
  print("중립")
}else{
  a <- "부정"
  b <- as.table(a,encoding="UTF-8")
  write.csv(b,file = "/root/SNS_Crawling/KoNLP/KoNLP_Result.csv",append=FALSE, fileEncoding="UTF-8")
  print("부정")
}

#sigmoid <- function(x){
#  1/(1+exp(-x))
#}

#x=seq(from=-5,to=5,by=0.1)
#plot(x,sigmoid(x),col="red")

#sessionInfo()
                
