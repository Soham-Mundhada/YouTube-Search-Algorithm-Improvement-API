import comments 
import sentiments 

comments_arr=comments.scrape_comments_with_replies("fkwx2TyvheI")
print("comments ----- ")
print(comments_arr)
comments_arr=sentiments.clean_text(comments_arr)
analysis=sentiments.get_Analysis(comments_arr)
print(analysis)
