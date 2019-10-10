library(rJava)
library(rvest)
library(KoNLP)
library(stringr)

pnames <- read.csv(file = '/root/pi200.csv',header=F, encoding = "UTF-8")
print(pnames)
rname <- c()


positive <- readLines(file("/root/SNS_Crawling/pos_pol_word.txt", encoding = "UTF-8"))
positive=positive[-1:-18]

negative <- readLines(file("/root/SNS_Crawling/neg_pol_word.txt", encoding = "UTF-8"))
negative=negative[-1:-18]

tryCatch(

for(pname in pnames[[1]]){
txt <- readLines(file(paste0("/root/SNS_Crawling/deduplication/",pname,"_dedupl.txt", sep=""),encoding = "UTF-8"))
#OO0
pos=SimplePos22(txt)
#OOO
pos.vec=unlist(pos)

#pos.vec<-gsub("[A-z]","",pos.vec) # 영어 삭제
#pos.vec<-gsub("/","",pos.vec) # /삭제
#pos.vec<-gsub("[+,ㄱ,ㄴ]","",pos.vec) # +,ㄱ,ㄴ삭제
#pos.vec<-gsub("^[:punct:]$","",pos.vec) # +,ㄱ,ㄴ삭제

pos.vec<-gsub("[^가-힣]","",pos.vec) # 한글이 아닌것 삭제

pos.vec<-pos.vec[-c(which(pos.vec=="" | pos.vec=="#"))]


#write.csv(pos.vec,paste("C:/Users/tlduf/Desktop/kosta/final project/SNS data/deduplication/",pname,"_dedupl.txt", sep=""),fileEncoding = "euc-kr")

pos.matches.num<-match(pos.vec,positive) # 긍정어 벡터 번호
neg.matches.num<-match(pos.vec,negative) # 부정어 벡터 번호

pos.matches.num ; neg.matches.num

pos.matches <- !is.na(pos.matches.num)
neg.matches <- !is.na(neg.matches.num)


pos.sum=sum(pos.matches)
neg.sum=sum(neg.matches)
pos.matches
neg.matches
pos.sum ; neg.sum


result <- pos.sum-neg.sum
result

if(result>0){
  rname <- c(rname,pname)
  print(paste(pname," : ","긍정"))
}else if(result==0){
  print(paste(pname," : ","중립"))
}else{
  print(paste(pname," : ","부정"))
}
}
,error = function(e)print("error")
,warning = function(w)print("warning")
,finally = NULL
)
print(rname)
savelocal = '/root'

if(!file.exists(paste(savelocal,"Rjname.csv"))){
  file.remove('/root/Rjname.csv')
}

setwd(savelocal)
write.csv(rname, file = "Rjname.csv",row.names = FALSE)

