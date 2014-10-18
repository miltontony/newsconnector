using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using System.IO.IsolatedStorage;
using System.Windows.Data;

namespace NewsWorldApp
{
    public partial class PivotPage1 : PhoneApplicationPage
    {
        public PivotPage1()
        {
            InitializeComponent();
            this.Loaded += new RoutedEventHandler(SettingsPage_Loaded);
        }

        private void SettingsPage_Loaded(object sender, RoutedEventArgs e)
        {
            IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
            if (settings.Contains("edition"))
            {
                if ((string)settings["edition"] == "southafrica")
                {
                    rbSouthAfrica.IsChecked = true;
                }
                else if ((string)settings["edition"] == "international")
                {
                    rbInternational.IsChecked = true;
                }
            }
        }

        private void btnSave_Click_1(object sender, RoutedEventArgs e)
        {
            if (Convert.ToBoolean(rbSouthAfrica.IsChecked) || Convert.ToBoolean(rbInternational.IsChecked))
            {
                var edition = string.Empty;

                if (Convert.ToBoolean(rbSouthAfrica.IsChecked))
                {
                    edition = "southafrica";
                }
                else
                {
                    edition = "international";
                }

                IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;
                if (!settings.Contains("edition"))
                {
                    settings.Add("edition", edition);
                }
                else
                {
                    settings["edition"] = edition;
                }
                settings.Save();
                NavigationService.Navigate(new Uri("/MainPage.xaml?mustUpdate=true", UriKind.Relative));
            }
        }

        private void onChecked(object sender, RoutedEventArgs e)
        {
            btnSave.IsEnabled = true;
        }
    }
}