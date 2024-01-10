// ハンバーガーメニューを作成する
import React, { useState } from 'react';
import Link from 'next/link'; 

const HamburgerMenu = () => {
    const [isMenuOpen, setMenuOpen] = useState(false);

    const toggleMenu = () => {
        setMenuOpen(!isMenuOpen);
    };

    return (
        <div className="fixed top-0 left-0 z-50">
            <div className="cursor-pointer p-4"  onClick={toggleMenu}>
                {/* ハンバーガーメニューの線 */}
                <div className="h-1 w-6 my-1 bg-blue-500"></div>
                <div className="h-1 w-6 my-1 bg-blue-500"></div>
                <div className="h-1 w-6 my-1 bg-blue-500"></div>
            </div>
            {isMenuOpen && (
                <div className="absolute left-0 mt-12 pl-4 w-48">
                <Link href="/" className="block px-4 py-2 md:text-2xl font-bold text-blue-500 hover:bg-gray-200">Home</Link>
                <Link href="/user-setting" className="block px-4 py-2 md:text-2xl  font-bold  text-blue-500 hover:bg-gray-200">設定</Link>
                <Link href="/get-plan" className="block px-4 py-2 md:text-2xl font-bold  text-blue-500 hover:bg-gray-200">計画立案</Link>
                <Link href="/learning-record" className="block px-4 md:text-2xl font-bold  py-2 text-blue-500 hover:bg-gray-200">学習記録</Link>
                <Link href="#" className="block px-4 py-2 md:text-2xl font-bold text-blue-500 hover:bg-gray-200">ログアウト</Link>
            </div>
            )}
        </div>
    );
};

export default HamburgerMenu;



// // hamburger.module.cssをインポート
// import React, { useState } from 'react';
// import Link from 'next/link'; 
// import styles from '../../styles/hamburger.module.css';

// const HamburgerMenu = () => {
//     const [isMenuOpen, setMenuOpen] = useState(false);

//     const toggleMenu = () => {
//         setMenuOpen(!isMenuOpen);
//     };

//     return (
//         <div className={styles.hamburgerMenu}>
//             <div className={styles.menuIcon} onClick={toggleMenu}>
//                 {/* ハンバーガーメニューの線 */}
//                 <div className={styles.bar}></div>
//                 <div className={styles.bar}></div>
//                 <div className={styles.bar}></div>
//             </div>
//             {isMenuOpen && (
//                 <div className={styles.menuContent}>
//                     <Link href="/">Home</Link>
//                     <Link href="/user-setting">設定</Link>
//                     <Link href="/get-plan">計画立案</Link>
//                     <Link href="/learning-record">学習記録</Link>
//                     <Link href="#">ログアウト</Link>
//                 </div>
//             )}
//         </div>
//     );
// };

// export default HamburgerMenu;