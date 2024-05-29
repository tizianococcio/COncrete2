/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:8000/:path*',
      },
    ]
  },
  experimental: {
    proxyTimeout: 360_000, /** 6 minutes for slow async requests */
  }
};

export default nextConfig;