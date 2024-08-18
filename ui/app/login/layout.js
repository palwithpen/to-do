// app/layout.js
import '../globals.css'; // Your global styles

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>
                    {children}
            </body>
        </html>
    );
}
