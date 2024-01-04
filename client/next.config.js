// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   reactStrictMode: true,
//   files: ['./styles/tailwind.css'],
//   async headers() {
//     return [
//       {
//         source: '/(.*)',
//         headers: [
//           {
//             key: 'Cross-Origin-Opener-Policy',
//             value: 'same-origin',
//           },
//         ],
//       },
//     ];
//   },
// };

// module.exports = nextConfig;


/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  files: ['./styles/tailwind.css'],
}
// async headers() { return [ { source: '/(.*)', headers: [ { key: 'Cross-Origin-Opener-Policy', value: 'same-origin', }, ], }, ]; 
module.exports = nextConfig
