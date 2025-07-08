import { Outlet, useLocation } from "react-router-dom";
import Header from "./Header";
import { AnimatePresence, motion } from "framer-motion";

const pageVariants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  in: {
    opacity: 1,
    y: 0,
  },
  out: {
    opacity: 0,
    y: -20,
  },
};

const pageTransition = {
  type: "tween" as const,
  ease: "anticipate" as const,
  duration: 0.4,
};

const Layout = () => {
  const { pathname } = useLocation();
  return (
    <>
      <Header />
      <AnimatePresence mode="wait">
        <motion.div
          key={pathname}
          initial="initial"
          animate="in"
          exit="out"
          variants={pageVariants}
          transition={pageTransition}
        >
          <Outlet />
        </motion.div>
      </AnimatePresence>
    </>
  );
};

export default Layout;
