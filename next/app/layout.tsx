import "./globals.css";
import { Public_Sans } from "next/font/google";

import { Navbar } from "@/components/Navbar";
import SessionProviderWrapper from "@/components/SessionProviderWrapper";

const publicSans = Public_Sans({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  
  return (
    <html lang="en">
      <head>
        <title>Scribbot</title>
        <link rel="shortcut icon" href="/images/favicon.ico" />
        <meta
          name="description"
          content="Starter template showing how to use LangChain in Next.js projects. See source code and deploy your own at https://github.com/langchain-ai/langchain-nextjs-template!"
        />
        <meta property="og:title" content="LangChain + Next.js Template" />
        <meta
          property="og:description"
          content="Starter template showing how to use LangChain in Next.js projects. See source code and deploy your own at https://github.com/langchain-ai/langchain-nextjs-template!"
        />
        <meta property="og:image" content="/images/og-image.png" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="LangChain + Next.js Template" />
        <meta
          name="twitter:description"
          content="Starter template showing how to use LangChain in Next.js projects. See source code and deploy your own at https://github.com/langchain-ai/langchain-nextjs-template!"
        />
        <meta name="twitter:image" content="/images/og-image.png" />
      </head>
      <body className={publicSans.className}>
        <div className="flex flex-col p-4 md:p-12 max-w-full max-h-full w-full h-full">

          <SessionProviderWrapper>
            {/* <Navbar></Navbar> */}
            {children}
          </SessionProviderWrapper>
        </div>
      </body>
    </html>
  );
}

