using Microsoft.Phone.Controls;
using Microsoft.Phone.Tasks;
using NewsWorldApp.ViewModels;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace NewsWorldApp
{
    [DataContract]
    public class Article
    {
        [DataMember]
        public string content { get; set; }
        [DataMember]
        public string source { get; set; }
        [DataMember]
        public string score { get; set; }
        [DataMember]
        public string link { get; set; }
        [DataMember]
        public string[] keywords { get; set; }
        [DataMember]
        public string title { get; set; }
        [DataMember]
        public string date { get; set; }
        [DataMember]
        public string image_url { get; set; }
        [DataMember]
        public string hash_key { get; set; }
        [DataMember]
        public Article[] similar { get; set; }

        public string similarCount {
            get
            {
                return String.Format("{0,12}", this.similar.Count() + "   similar");
            }
        }
    }

    public class NewsCategory
    {
        public string url { get; set; }
        public int pageNo { get; set; }

        public NewsCategory()
        {
            this.pageNo = 1;
        }
    }

    [DataContract]
    public class Headlines
    {
        [DataMember]
        public Article[] news { get; set; }

        [DataMember]
        public Article[] entertainment { get; set; }

        [DataMember]
        public Article[] finance { get; set; }

        [DataMember]
        public Article[] sports { get; set; }

    }


    public class HeadlinesObservable
    {
        public ObservableCollection<Article> news { get; set; }

        public ObservableCollection<Article> entertainment { get; set; }

        public ObservableCollection<Article> finance { get; set; }

        public ObservableCollection<Article> sports { get; set; }

        public HeadlinesObservable()
        {
            this.news = new ObservableCollection<Article>();
            this.sports = new ObservableCollection<Article>();
            this.finance = new ObservableCollection<Article>();
            this.entertainment = new ObservableCollection<Article>();
        }

        public void update(Headlines obj)
        {
            updateCollection(news, obj.news);
            updateCollection(sports, obj.sports);
            updateCollection(finance, obj.finance);
            updateCollection(entertainment, obj.entertainment);
        }

        private void updateCollection(ObservableCollection<Article> collection, IList<Article> items)
        {
            collection.Clear();
            if (items != null)
            {
                foreach (var item in items)
                {
                    collection.Add(item);
                }
            }
        }

        public void Clear()
        {
            this.news.Clear();
            this.sports.Clear();
            this.entertainment.Clear();
            this.finance.Clear();
        }
    }


    [DataContract]
    public class NewsWorldResult
    {
        [DataMember]
        public int cat { get; set; }

        [DataMember]
        public Article[] articles { get; set; }

    }

    public class Utils
    {
        public static bool loadSimilar(object sender, ArticleViewModel viewModel)
        {
            var listBox = sender as LongListSelector;

            if (listBox != null && listBox.SelectedItem != null)
            {
                // Get the SyndicationItem that was tapped.
                Article sItem = (Article)listBox.SelectedItem;
                if (sItem.similar.Any())
                {
                    viewModel.LoadSimilar(sItem);
                    listBox.SelectedItem = null;
                    return true;
                }

                updateListBox(sender);
            }
            listBox.SelectedItem = null;
            return false;
        }

        public static void updateListBox(object sender)
        {
            var listBox = sender as LongListSelector;

            if (listBox != null && listBox.SelectedItem != null)
            {
                // Get the SyndicationItem that was tapped.
                Article sItem = (Article)listBox.SelectedItem;

                // Set up the page navigation only if a link actually exists in the feed item.
                if (sItem.link != null)
                {
                    // Get the associated URI of the feed item.
                    Uri uri = new Uri(sItem.link);

                    // Create a new WebBrowserTask Launcher to navigate to the feed item. 
                    // An alternative solution would be to use a WebBrowser control, but WebBrowserTask is simpler to use. 
                    WebBrowserTask webBrowserTask = new WebBrowserTask();
                    webBrowserTask.Uri = uri;
                    webBrowserTask.Show();
                }

                listBox.SelectedItem = null;
            }
        }

        public static T Deserialize<T>(string json)
        {
            var obj = Activator.CreateInstance<T>();
            using (var memoryStream = new MemoryStream(Encoding.Unicode.GetBytes(json)))
            {
                var serializer = new DataContractJsonSerializer(obj.GetType());
                obj = (T)serializer.ReadObject(memoryStream);
                return obj;
            }
        }
    }
}
