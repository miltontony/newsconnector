using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using NewsWorldApp.ViewModels;
using Microsoft.Phone.Tasks;

namespace NewsWorldApp
{
    public partial class Similar : PhoneApplicationPage
    {
        public Similar()
        {
            InitializeComponent();
            DataContext = App.AppViewModel;
        }

        private void feedListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            Utils.updateListBox(sender);
        }

        private void StackPanel_Tap(object sender, System.Windows.Input.GestureEventArgs e)
        {
            // Get the SyndicationItem that was tapped.
            Article sItem = App.AppViewModel.Similar;

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
        }
    }
}