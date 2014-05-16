using System;
using System.Net;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using NewsWorldApp.ViewModels;
using System.Windows.Data;
using System.IO.IsolatedStorage;

namespace NewsWorldApp
{
    public partial class MainPage : PhoneApplicationPage
    {
        int _offsetKnob = 20;
        //ArticleViewModel _viewModel;

        // Constructor
        public MainPage()
        {
            InitializeComponent();

            // Set the data context of the listbox control to the sample data
            DataContext = App.AppViewModel;
            //Init();
            //_viewModel = (ArticleViewModel)Resources["viewModel"];
            feedListBox.ItemRealized += feedListBox_ItemRealized;
            sportsListBox.ItemRealized += sportsListBox_ItemRealized;
            financeListBox.ItemRealized += financeListBox_ItemRealized;
            entertainmentListBox.ItemRealized += entertainmentListBox_ItemRealized;
            this.Loaded += new RoutedEventHandler(MainPage_Loaded);
        }

        void MainPage_Loaded(object sender, RoutedEventArgs e)
        {
            var progressIndicator = SystemTray.ProgressIndicator;
            if (progressIndicator != null)
            {
                return;
            }

            progressIndicator = new ProgressIndicator();

            SystemTray.SetProgressIndicator(this, progressIndicator);

            var binding = new Binding("IsLoading") { Source = App.AppViewModel};
            BindingOperations.SetBinding(
                progressIndicator, ProgressIndicator.IsVisibleProperty, binding);

            binding = new Binding("IsLoading") { Source = App.AppViewModel };
            BindingOperations.SetBinding(
                progressIndicator, ProgressIndicator.IsIndeterminateProperty, binding);

            progressIndicator.Text = "Loading new articles...";

            CheckEditionSettings();
        }

        private void CheckEditionSettings()
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (!settings.Contains("edition"))
            {
                NavigationService.Navigate(new Uri("/Settings.xaml", UriKind.Relative));
            }
            else
            {
                if ((string)settings["edition"] == "southafrica")
                {
                    pvtFinance.Visibility = System.Windows.Visibility.Visible;
                    financeStack.Visibility = System.Windows.Visibility.Visible;
                }
                else
                {
                    pvtFinance.Visibility = System.Windows.Visibility.Collapsed;
                    financeStack.Visibility = System.Windows.Visibility.Collapsed;
                }
            }
        }

        // This method determines whether the user has navigated to the application after the application was tombstoned.
        protected override void OnNavigatedTo(System.Windows.Navigation.NavigationEventArgs e)
        {
            if (!App.ViewModel.IsDataLoaded)
            {
                App.ViewModel.LoadData();
            }

            string mustUpdate = "";
            if (NavigationContext.QueryString.TryGetValue("mustUpdate", out mustUpdate))
            {
                if (mustUpdate == "true")
                {
                    App.AppViewModel.LoadAllArticles();
                }

            }
        }

        // The SelectionChanged handler for the feed items 
        private void feedListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (Utils.loadSimilar(sender, App.AppViewModel))
            {
                NavigationService.Navigate(new Uri("/Similar.xaml", UriKind.Relative));
            }
        }

        private void feedListBox_ItemRealized(object sender, ItemRealizationEventArgs e)
        {
            resultListBox_ItemRealized(sender, 1, e); 
        }

        private void sportsListBox_ItemRealized(object sender, ItemRealizationEventArgs e)
        {
            resultListBox_ItemRealized(sender, 2, e);
        }

        private void financeListBox_ItemRealized(object sender, ItemRealizationEventArgs e)
        {
            resultListBox_ItemRealized(sender, 3, e);
        }

        private void entertainmentListBox_ItemRealized(object sender, ItemRealizationEventArgs e)
        {
            resultListBox_ItemRealized(sender, 4, e);
        }

        private void resultListBox_ItemRealized(object sender, int cat, ItemRealizationEventArgs e)
        {
            var listBox = sender as LongListSelector;

            if (listBox != null )
            {
                if (!App.AppViewModel.IsLoading && listBox.ItemsSource != null && listBox.ItemsSource.Count >= _offsetKnob)
                {
                    if (e.ItemKind == LongListSelectorItemKind.Item)
                    {
                        if ((e.Container.Content as Article).Equals(listBox.ItemsSource[listBox.ItemsSource.Count - _offsetKnob]))
                        {
                            App.AppViewModel.LoadArticles(cat);
                        }
                    }
                }
            }
        }

        private void ApplicationBarMenuItem_Click_1(object sender, EventArgs e)
        {
            NavigationService.Navigate(new Uri("/Settings.xaml", UriKind.Relative));
        }

        private void ApplicationBarIconButton_Click_1(object sender, EventArgs e)
        {
            App.AppViewModel.LoadAllArticles();
        }
    }
}