const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})
module.exports = withBundleAnalyzer({})

module.exports = {
  crossOrigin: 'anonymous',
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/:path*', // Replace with your Python server's URL and port
      },
    ]
  },
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
      domains: ['127.0.0.1', 'res.cloudinary.com'],
  },
  async redirects() {
      return [{
          source: '/',
          destination: '/login',
          permanent: true
      }]
  },
  /** @type {import('next').NextConfig} */

  async headers() {
      return [
          {
              // matching all API routes
              // source: "/api/:path*",
              source: '/',
 
              headers: [
                  { key: "Access-Control-Allow-Credentials", value: "true" },
                  { key: "Access-Control-Allow-Origin", value: "*" }, // replace this your actual origin
                  { key: "Access-Control-Allow-Methods", value: "GET,DELETE,PATCH,POST,PUT" },
                  { key: "Access-Control-Allow-Headers", value: "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version" },
              ]
          }
      ]
  }

}
module.exports = nextConfig