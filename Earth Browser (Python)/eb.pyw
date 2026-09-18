import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class KEsearchApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Earth Browser (Chromium Powered)")
        self.resize(1200, 800)
        self.setWindowIcon(QIcon("favicon.ico"))

        self.profile = QWebEngineProfile("EarthBrowserProfile", self)
        self.profile.setPersistentStoragePath(r".\bdata")
        self.profile.setCachePath(r".\bdata\cache")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)

        nav_layout = QHBoxLayout()

        self.back_btn = QPushButton("←")
        self.back_btn.setMaximumWidth(40)
        self.back_btn.clicked.connect(self.navigate_back)
        nav_layout.addWidget(self.back_btn)

        self.fwd_btn = QPushButton("→")
        self.fwd_btn.setMaximumWidth(40)
        self.fwd_btn.clicked.connect(self.navigate_forward)
        nav_layout.addWidget(self.fwd_btn)

        self.refresh_btn = QPushButton("⟳")
        self.refresh_btn.setMaximumWidth(40)
        self.refresh_btn.clicked.connect(self.navigate_refresh)
        nav_layout.addWidget(self.refresh_btn)

        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText(
            "Enter URL or search query and press Enter..."
        )
        self.address_bar.returnPressed.connect(self.address_bar_submitted)
        nav_layout.addWidget(self.address_bar)

        go_btn = QPushButton("Go")
        go_btn.setStyleSheet(
            "background-color: #0066cc; color: white; font-weight: bold; padding:"
            " 5px 12px;"
        )
        go_btn.clicked.connect(self.address_bar_submitted)
        nav_layout.addWidget(go_btn)

        new_tab_btn = QPushButton("+ New Tab")
        new_tab_btn.clicked.connect(lambda: self.add_tab())
        nav_layout.addWidget(new_tab_btn)

        main_layout.addLayout(nav_layout)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        main_layout.addWidget(self.tabs)

        self.add_tab("https://thedoggybrad.github.io/simple_web_homepage/")

    def add_tab(
        self, url_str="https://thedoggybrad.github.io/simple_web_homepage/"
    ):
        page = QWebEnginePage(self.profile, self)
        web_view = QWebEngineView()
        web_view.setPage(page)
        web_view.setUrl(QUrl(url_str))

        # Connect signals to update address bar and tab titles dynamically
        web_view.urlChanged.connect(
            lambda url, wv=web_view: self.update_address_bar(wv, url)
        )
        web_view.titleChanged.connect(
            lambda title, wv=web_view: self.update_tab_title(wv, title)
        )

        index = self.tabs.addTab(web_view, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            # If it's the last tab, reset it to the home page instead of closing the app
            current_view = self.tabs.currentWidget()
            if isinstance(current_view, QWebEngineView):
                current_view.setUrl(
                    QUrl(
                        "https://thedoggybrad.github.io/simple_web_homepage/"
                    )
                )

    def tab_changed(self, index):
        current_view = self.tabs.currentWidget()
        if isinstance(current_view, QWebEngineView):
            self.address_bar.setText(current_view.url().toString())

    def update_address_bar(self, web_view, url):
        if self.tabs.currentWidget() == web_view:
            self.address_bar.setText(url.toString())

    def update_tab_title(self, web_view, title):
        index = self.tabs.indexOf(web_view)
        if index != -1 and title:
            display_title = (title[:15] + "..") if len(title) > 15 else title
            self.tabs.setTabText(index, display_title)

    def navigate_back(self):
        current_view = self.tabs.currentWidget()
        if isinstance(current_view, QWebEngineView):
            current_view.back()

    def navigate_forward(self):
        current_view = self.tabs.currentWidget()
        if isinstance(current_view, QWebEngineView):
            current_view.forward()

    def navigate_refresh(self):
        current_view = self.tabs.currentWidget()
        if isinstance(current_view, QWebEngineView):
            current_view.reload()

    def address_bar_submitted(self):
        text = self.address_bar.text().strip()
        if not text:
            return

        current_view = self.tabs.currentWidget()
        if not isinstance(current_view, QWebEngineView):
            return

        # Determine if input is a direct URL or a search query
        if (
            text.startswith("http://")
            or text.startswith("https://")
            or ("." in text and " " not in text and not text.startswith(" "))
        ):
            url = text if text.startswith("http") else "https://" + text
        else:
            url = f"https://duckduckgo.com{text}"

        current_view.setUrl(QUrl(url))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KEsearchApp()
    window.show()
    sys.exit(app.exec())
