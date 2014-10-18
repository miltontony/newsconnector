using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Threading;
using System.IO.IsolatedStorage;
using System.Windows.Navigation;

namespace NewsWorldApp.ViewModels
{
    public class ArticleViewModel : INotifyPropertyChanged
    {
        private bool isLoading = false;
        private Object loadingLock;

        public bool IsLoading
        {
            get
            {
                return isLoading;
            }
            set
            {
                isLoading = value;
                Deployment.Current.Dispatcher.BeginInvoke(() =>
                {
                    NotifyPropertyChanged("IsLoading");
                });

            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void NotifyPropertyChanged(String propertyName)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (null != handler)
            {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        public ArticleViewModel()
        {
            if (!DesignerProperties.IsInDesignTool)
            {
                loadingLock = new Object();
                this.Headlines= new HeadlinesObservable();
                this.NewsCollection = new ObservableCollection<Article>();
                this.SportsCollection = new ObservableCollection<Article>();
                this.FinanceCollection = new ObservableCollection<Article>();
                this.EntertainmentCollection = new ObservableCollection<Article>();
                this.SimilarCollection = new ObservableCollection<Article>();
                this.IsLoading = false;

                AutoLoadArticles();
            }
        }

        public void AutoLoadArticles()
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (settings.Contains("edition"))
            {
                LoadFromSettings();
                LoadAllArticles();
            }
        }

        public void LoadAllArticles()
        {
            for (int i = 1; i <= 6; i++)
            {
                this.Categories[i].pageNo = 1;
            }
            clearCollections();

            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (settings.Contains("edition"))
            {
                if ((string)settings["edition"] == "southafrica")
                {
                    new Thread(new ThreadStart(LoadHeadlines)).Start();
                    new Thread(new ThreadStart(LoadNewsArticles)).Start();
                    new Thread(new ThreadStart(LoadSportsArticles)).Start();
                    new Thread(new ThreadStart(LoadFinanceArticles)).Start();
                    new Thread(new ThreadStart(LoadEntertainmentArticles)).Start();
                }
                else
                {
                    new Thread(new ThreadStart(LoadIHeadlines)).Start();
                    new Thread(new ThreadStart(LoadINewsArticles)).Start();
                    new Thread(new ThreadStart(LoadISportsArticles)).Start();
                    new Thread(new ThreadStart(LoadEntertainmentArticles)).Start();
                }
            }
        }

        private void LoadFromSettings()
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (settings.Contains("headlines"))
            {
                var headlines = (Headlines)settings["headlines"];
                this.Headlines.update(headlines);
            }
            if (settings.Contains("newsCollection"))
            {
                updateCollection(this.NewsCollection, (IList<Article>)settings["newsCollection"]);
            }
            if (settings.Contains("sportsCollection"))
            {
                updateCollection(this.SportsCollection, (IList<Article>)settings["sportsCollection"]);
            }
            if (settings.Contains("financeCollection"))
            {
                updateCollection(this.FinanceCollection, (IList<Article>)settings["financeCollection"]);
            }
            if (settings.Contains("entertainmentCollection"))
            {
                updateCollection(this.EntertainmentCollection, (IList<Article>)settings["entertainmentCollection"]);
            }
        }

        private void LoadNewsArticles()
        {
            LoadArticles(1);
        }

        private void LoadSportsArticles()
        {
            LoadArticles(2);
        }

        private void LoadFinanceArticles()
        {
            LoadArticles(3);
        }

        private void LoadEntertainmentArticles()
        {
            LoadArticles(4);
        }

        private void LoadINewsArticles()
        {
            LoadArticles(5);
        }

        private void LoadISportsArticles()
        {
            LoadArticles(6);
        }

        Dictionary<int, NewsCategory> Categories= new Dictionary<int, NewsCategory>()
        {
            { 1, new NewsCategory {url="http://newsworld.co.za/api/news/"} },
            { 2, new NewsCategory {url="http://newsworld.co.za/api/sports/"} },
            { 3, new NewsCategory {url="http://newsworld.co.za/api/finance/"} },
            { 4, new NewsCategory {url="http://newsworld.co.za/api/entertainment/"} },
            { 5, new NewsCategory {url="http://newsworld.co.za/api/inews/"} },
            { 6, new NewsCategory {url="http://newsworld.co.za/api/isports/"} }
        };

        #region News Collections

        public HeadlinesObservable Headlines
        {
            get;
            private set;
        }

        public ObservableCollection<Article> NewsCollection
        {
            get;
            private set;
        }

        public ObservableCollection<Article> SportsCollection
        {
            get;
            private set;
        }

        public ObservableCollection<Article> FinanceCollection
        {
            get;
            private set;
        }

        public ObservableCollection<Article> EntertainmentCollection
        {
            get;
            private set;
        }

        public Article Similar
        {
            get;
            private set;
        }

        public ObservableCollection<Article> SimilarCollection
        {
            get;
            private set;
        }

        #endregion

        public void LoadHeadlines()
        {
            lock (loadingLock)
            {
                IsLoading = true;

                WebClient webClient = new WebClient();
                webClient.DownloadStringCompleted += new DownloadStringCompletedEventHandler(webClient_DownloadHeadlinesCompleted);
                webClient.DownloadStringAsync(new System.Uri("http://newsworld.co.za/api/headlines/"));
            }
        }

        public void LoadIHeadlines()
        {
            lock (loadingLock)
            {
                IsLoading = true;

                WebClient webClient = new WebClient();
                webClient.DownloadStringCompleted += new DownloadStringCompletedEventHandler(webClient_DownloadHeadlinesCompleted);
                webClient.DownloadStringAsync(new System.Uri("http://newsworld.co.za/api/iheadlines/"));
            }
        }

        public void LoadArticles(int cat)
        {
            lock (loadingLock)
            {
                var category = this.Categories[cat];
                IsLoading = true;

                WebClient webClient = new WebClient();
                webClient.DownloadStringCompleted += new DownloadStringCompletedEventHandler(webClient_DownloadStringCompleted);
                webClient.DownloadStringAsync(new System.Uri(category.url + "?page=" + category.pageNo));

                category.pageNo++;
            }
        }

        public void LoadSimilar(Article article)
        {
            this.SimilarCollection.Clear();
            this.Similar = article;
            updateCollection(this.SimilarCollection, article.similar);
        }

        private void webClient_DownloadStringCompleted(object sender, DownloadStringCompletedEventArgs e)
        {
            if (e.Error != null)
            {
                Deployment.Current.Dispatcher.BeginInvoke(() =>
                {
                    MessageBox.Show(e.Error.Message);
                });
            }
            else
            {
                var parsedData = Utils.Deserialize<NewsWorldResult>(e.Result);
                Deployment.Current.Dispatcher.BeginInvoke(() =>
                {
                    switch (parsedData.cat)
                    {
                        case 1:
                            updateCollection(this.NewsCollection, parsedData.articles);
                            saveCollection(parsedData.articles, "newsCollection");
                            break;

                        case 2:
                            updateCollection(this.SportsCollection, parsedData.articles);
                            saveCollection(parsedData.articles, "sportsCollection");
                            break;

                        case 3:
                            updateCollection(this.FinanceCollection, parsedData.articles);
                            saveCollection(parsedData.articles, "financeCollection");
                            break;

                        case 4:
                            updateCollection(this.EntertainmentCollection, parsedData.articles);
                            saveCollection(parsedData.articles, "entertainmentCollection");
                            break;

                        case 5:
                            updateCollection(this.NewsCollection, parsedData.articles);
                            saveCollection(parsedData.articles, "newsCollection");
                            break;

                        case 6:
                            updateCollection(this.SportsCollection, parsedData.articles);
                            saveCollection(parsedData.articles, "sportsCollection");
                            break;
                    }

                    IsLoading = false;
                });
            }
        }

        private void webClient_DownloadHeadlinesCompleted(object sender, DownloadStringCompletedEventArgs e)
        {
            if (e.Error != null)
            {
                Deployment.Current.Dispatcher.BeginInvoke(() =>
                {
                    MessageBox.Show(e.Error.Message);
                });
            }
            else
            {
                var parsedData = Utils.Deserialize<Headlines>(e.Result);
                Deployment.Current.Dispatcher.BeginInvoke(() =>
                {
                    this.Headlines.update(parsedData);

                    IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
                    if (!settings.Contains("headlines"))
                    {
                        settings.Add("headlines", parsedData);
                    }
                    else
                    {
                        settings["headlines"] = parsedData;
                    }
                    settings.Save();

                    IsLoading = false;
                });
            }
        }

        public static void updateCollection(ObservableCollection<Article> collection, IList<Article> items)
        {
            if (collection.Count() == 10)
            {
                collection.Clear();
            }

            if (items != null)
            {
                foreach (var item in items)
                {
                    collection.Add(item);
                }
            }
        }

        private void saveCollection(IList<Article> items, string storeName)
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (!settings.Contains(storeName))
            {
                settings.Add(storeName, items.Take(10).ToList());
            }
            else
            {
                settings[storeName] = items.Take(10).ToList();
            }
            settings.Save();
        }

        private void clearCollections()
        {
            NewsCollection.Clear();
            SportsCollection.Clear();
            FinanceCollection.Clear();
            EntertainmentCollection.Clear();
            Headlines.Clear();
        }
    }
}
