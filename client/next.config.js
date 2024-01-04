/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  async rewrites() {
    return [
      {
        source: '/api/create_user',
        destination: 'http://localhost:8000/create_user',
      },
    ];
  },
}


module.exports = nextConfig
