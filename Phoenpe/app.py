from distutils.errors import PreprocessError
import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.set_page_config(layout='wide')
st.sidebar.title("Phonepe Transaction Analysis")
st.title("TOP STATISTICS")


file = st.sidebar.file_uploader('Upload CSV', type=['csv'])

if file is not None:
    # Read the uploaded file
    data = pd.read_csv(file)
    data.drop(columns=["Unnamed: 2"], inplace=True, errors='ignore')
    df = preprocessor.preprocess(data)
    st.dataframe(df)
    
    # fetch unique users
    user_list = df['Name'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt Name",user_list)
    
    
    
    if st.sidebar.button("Show Analysis"):
        num_trans, deb, cre, top_debit_persons, top_credit_persons = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3 = st.columns(3)
        
        with col1:
            st.header("No. of Transaction")
            st.subheader(num_trans)
        with col2:
            st.header("Total Debit")
            st.subheader(deb)
        with col3:
            st.header("Total Credit")
            st.subheader(cre)
        
        
        col4,col4 = st.columns(2)      
        with col1:
            top_debit_persons.columns = ['Name', 'Debit Amount']
            st.write("Top 5 Debit:")
            st.write(top_debit_persons)
            
        with col2:
            top_debit_persons.columns = ['Name', 'Debit Amount']
            st.write("Top 5 Credit:")
            st.write(top_credit_persons)
        
        
        st.title("Total amount Spend by Month")
        helper.total_amount_spent_by_month(selected_user, df)
        
        st.title("Percentage of Transaction Types")
        helper.Percentage_of_Transaction_Types(selected_user, df)

        st.title("Daily amount spend")
        helper.Dailyamountspend(selected_user, df)
        
        st.title("Day of week")
        helper.Dayofweek(selected_user, df)




    # # Grouping the data by month and summing the amounts
    # monthly_data = df.groupby('Month')['Amount'].sum()
    # plt.figure(figsize=(16, 6))
    # colors = plt.cm.tab20c.colors[:len(monthly_data)]
    # bars = plt.bar(monthly_data.index, monthly_data.values, color=colors, edgecolor='black')
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.xlabel('Month', fontsize=12, fontweight='bold')
    # plt.ylabel('Total Amount', fontsize=12, fontweight='bold')
    # plt.title('Total Amount Spent by Month', fontsize=14, fontweight='bold')
    # plt.xticks(rotation=45)
    # plt.yticks(fontsize=10) 
    # for bar in bars:
    #     yval = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width() / 2, yval + 20, round(yval, 2), ha='center', va='bottom')
    # st.pyplot(plt)






    #     # monthly timeline
    #     st.title("Monthly Timeline")
    #     timeline = helper.monthly_timeline(selected_user,df)
    #     fig,ax = plt.subplots()
    #     ax.plot(timeline['time'], timeline['message'],color='green')
    #     plt.xticks(rotation='vertical')
    #     st.pyplot(fig)

    #             # daily timeline
    #     st.title("Daily Timeline")
    #     daily_timeline = helper.daily_timeline(selected_user, df)
    #     fig, ax = plt.subplots()
    #     ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
    #     plt.xticks(rotation='vertical')
    #     st.pyplot(fig)

    #     # activity map
    #     st.title('Activity Map')
    #     col1,col2 = st.columns(2)

    #     with col1:
    #         st.header("Most busy day")
    #         busy_day = helper.week_activity_map(selected_user,df)
    #         fig,ax = plt.subplots()
    #         ax.bar(busy_day.index,busy_day.values,color='purple')
    #         plt.xticks(rotation='vertical')
    #         st.pyplot(fig)

    #     with col2:
    #         st.header("Most busy month")
    #         busy_month = helper.month_activity_map(selected_user, df)
    #         fig, ax = plt.subplots()
    #         ax.bar(busy_month.index, busy_month.values,color='orange')
    #         plt.xticks(rotation='vertical')
    #         st.pyplot(fig)

    #     st.title("Weekly Activity Map")
    #     user_heatmap = helper.activity_heatmap(selected_user,df)
    #     fig,ax = plt.subplots()
    #     ax = sns.heatmap(user_heatmap)
    #     st.pyplot(fig)


    #     # finding the busiest users in the group(Group level)
    #     if selected_user == 'Overall':
    #         st.title('Most Active Users')
    #         x,new_df = helper.most_busy_users(df)
    #         fig, ax = plt.subplots()
    #         col1, col2 = st.columns(2)
    #         with col1:
    #             ax.bar(x.index, x.values,color='red')
    #             plt.xticks(rotation='vertical')
    #             st.pyplot(fig)
    #         with col2:
    #             st.dataframe(new_df,width=700, height=768)
    #     # WordCloud
    #     st.title("Wordcloud:- Most frequence word")
    #     df_wc = helper.create_wordcloud(selected_user,df)
    #     fig,ax = plt.subplots()
    #     ax.imshow(df_wc)
    #     st.pyplot(fig)

    #             # most common words
    #     most_common_df = helper.most_common_words(selected_user,df)

    #     fig,ax = plt.subplots()

    #     ax.barh(most_common_df[0],most_common_df[1])
    #     plt.xticks(rotation='vertical')

    #     st.title('Most commmon words')
    #     st.pyplot(fig)

    #            # emoji analysis
    #     emoji_df = helper.emoji_helper(selected_user,df)
    #     st.title("Emoji Analysis")

    #     col1,col2 = st.columns(2)

    #     with col1:
    #         st.dataframe(emoji_df,width=700, height=786)
    #     with col2:
    #         fig,ax = plt.subplots()
    #         ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
    #         st.pyplot(fig)