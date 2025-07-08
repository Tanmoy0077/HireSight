import { Link } from "react-router-dom";
import {
  FileText,
  BarChart2,
  Github,
  ClipboardList,
  CheckCircle,
} from "lucide-react";
import { motion } from "framer-motion";

export default function Homepage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section
        id="home"
        className="py-20 bg-gradient-to-b from-blue-50 to-transparent text-center"
      >
        <div className="container mx-auto px-4 flex flex-col items-center">
          <motion.h1
            className="text-5xl font-extrabold mb-6 text-gray-800 leading-tight"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            Streamline Your Hiring with
            <span className="text-blue-600 block mt-2">
              AI-Powered Insights
            </span>
          </motion.h1>
          <motion.p
            className="text-lg text-gray-600 mb-8 max-w-2xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            Go beyond the resume. Our tool provides deep analysis, generates
            interview plans, and assesses candidate risk to help you build the
            perfect team.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <Link
              to="/upload"
              className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg font-semibold hover:bg-blue-700 transition flex items-center gap-2 shadow-lg"
            >
              <FileText className="w-5 h-5" />
              Get Started
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <motion.section
        id="features"
        className="py-16 bg-white flex flex-col items-center"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, amount: 0.3 }}
        transition={{ staggerChildren: 0.2 }}
      >
        <h2 className="text-3xl font-bold mb-12 text-gray-800">
          A Smarter Way to Hire
        </h2>
        <div className="flex flex-wrap justify-center gap-10 max-w-6xl mx-auto">
          <FeatureCard
            icon={<BarChart2 className="w-8 h-8 text-blue-500" />}
            title="In-Depth Candidate Review"
            desc="Get a holistic view with an overall fitness score, skill matching, and performance metrics."
          />
          <FeatureCard
            icon={<ClipboardList className="w-8 h-8 text-green-500" />}
            title="Automated Interview Plans"
            desc="Generate tailored interview questions and a structured onboarding plan for every candidate."
          />
          <FeatureCard
            icon={<CheckCircle className="w-8 h-8 text-yellow-500" />}
            title="Strategic Hiring Insights"
            desc="Identify key strengths, critical skill gaps, and potential risk factors to make informed decisions."
          />
        </div>
      </motion.section>

      {/* About Section */}
      <section id="about" className="py-16 bg-blue-50 text-center">
        <h2 className="text-3xl font-bold mb-5 text-gray-800">About</h2>
        <p className="max-w-xl mx-auto text-lg text-gray-700 mb-8">
          HireSight is an open-source tool built for HR professionals and hiring
          managers to streamline the evaluation process. Make faster, smarter,
          and more confident hiring decisions with AI-driven insights.
        </p>
        <a
          href="https://github.com/Tanmoy0077/HireSight"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 bg-gray-800 text-white px-6 py-3 rounded-full font-medium hover:bg-gray-700 transition"
        >
          <Github className="w-5 h-5" />
          View on GitHub
        </a>
      </section>
    </div>
  );
}

// Feature Card Component
function FeatureCard({
  icon,
  title,
  desc,
}: {
  icon: React.ReactNode;
  title: string;
  desc: string;
}) {
  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <motion.div
      className="bg-white p-8 rounded-2xl w-80 shadow-md border border-gray-100 flex flex-col items-center hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
      variants={cardVariants}
    >
      <div className="mb-4">{icon}</div>
      <h3 className="font-semibold text-xl mb-2 text-gray-800">{title}</h3>
      <p className="text-gray-600 text-center">{desc}</p>
    </motion.div>
  );
}
