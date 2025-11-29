import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Pill, 
  Truck, 
  Megaphone, 
  Menu, 
  X, 
  CheckCircle2, 
  ArrowRight, 
  Clock, 
  AlertTriangle, 
  Server, 
  Database, 
  Cpu, 
  Share2,
  ShieldCheck,
  Zap,
  HeartPulse,
  Users,
  Lock,
  Stethoscope
} from 'lucide-react';

/**
 * HealthForce Goa - Multi-Page Experience
 * Update: Enhanced Login Page with role-specific "Active Alerts" context.
 */

// --- GLOBAL STYLES FOR ANIMATIONS ---
const GlobalStyles = () => (
  <style>{`
    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }
    .animate-float {
      animation: float 6s ease-in-out infinite;
    }
    .animate-float-delayed {
      animation: float 6s ease-in-out 3s infinite;
    }
    .animate-in {
      animation-duration: 0.6s;
      animation-fill-mode: both;
    }
    .fade-in {
      animation-name: fadeIn;
    }
    .slide-in-from-bottom-4 {
      animation-name: slideInBottom;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes slideInBottom {
      from { transform: translateY(20px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
  `}</style>
);

// --- COMPONENTS ---

const Navbar = ({ currentPage, setPage, isScrolled }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { id: 'home', label: 'Platform' },
    { id: 'agents', label: 'Agents' },
    { id: 'architecture', label: 'Architecture' },
    { id: 'impact', label: 'Impact' },
  ];

  return (
    <nav className={`fixed w-full z-50 transition-all duration-300 ${isScrolled ? 'bg-white/90 backdrop-blur-md shadow-sm border-b border-gray-100' : 'bg-transparent'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <div 
            className="flex-shrink-0 flex items-center gap-2 cursor-pointer"
            onClick={() => setPage('home')}
          >
            <div className="w-8 h-8 bg-black rounded-lg flex items-center justify-center text-white font-bold text-xl">H</div>
            <span className="text-2xl font-bold tracking-tighter">HealthForce Goa.</span>
          </div>
          
          {/* Desktop Menu */}
          <div className="hidden md:flex space-x-8 items-center">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => setPage(link.id)}
                className={`text-sm font-medium transition-colors ${currentPage === link.id ? 'text-black font-bold' : 'text-gray-600 hover:text-black'}`}
              >
                {link.label}
              </button>
            ))}
          </div>

          {/* CTA */}
          <div className="hidden md:flex items-center space-x-4">
            <button 
                onClick={() => setPage('login')}
                className="text-sm font-semibold hover:text-gray-600"
            >
                Log in
            </button>
            <button 
              onClick={() => setPage('demo')}
              className="bg-black text-white px-6 py-2.5 rounded-full text-sm font-semibold hover:bg-gray-800 transition-all hover:shadow-lg hover:-translate-y-0.5"
            >
              Book Demo
            </button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button 
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-gray-500 hover:text-black focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-white border-b border-gray-100 absolute top-20 left-0 w-full px-4 pt-2 pb-6 shadow-xl animate-in fade-in slide-in-from-bottom-4">
          <div className="flex flex-col space-y-4 mt-4">
            {navLinks.map((link) => (
              <button
                key={link.id}
                onClick={() => { setPage(link.id); setMobileMenuOpen(false); }}
                className={`text-left text-lg font-medium ${currentPage === link.id ? 'text-black' : 'text-gray-600'}`}
              >
                {link.label}
              </button>
            ))}
            <button 
              onClick={() => { setPage('login'); setMobileMenuOpen(false); }}
              className="text-left text-lg font-medium text-gray-600"
            >
              Log in
            </button>
            <button 
              onClick={() => { setPage('demo'); setMobileMenuOpen(false); }}
              className="bg-black text-white px-6 py-3 rounded-xl text-center font-semibold mt-4"
            >
              Book Demo
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};

const Footer = ({ setPage }) => (
  <footer className="bg-white border-t border-gray-200 pt-16 pb-8">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex flex-col md:flex-row justify-between items-start gap-12 mb-12">
        <div className="max-w-xs">
            <span className="text-2xl font-bold tracking-tighter mb-4 block">HealthForce Goa.</span>
            <p className="text-gray-500 text-sm leading-relaxed">
                Empowering healthcare systems with predictive intelligence and automated logistics.
            </p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-12 w-full md:w-auto">
            <div>
                <h4 className="font-bold mb-4">Product</h4>
                <ul className="space-y-2 text-sm text-gray-500">
                    <li><button onClick={() => setPage('agents')} className="hover:text-black text-left">Agents</button></li>
                    <li><button onClick={() => setPage('architecture')} className="hover:text-black text-left">Integrations</button></li>
                    <li><button onClick={() => setPage('impact')} className="hover:text-black text-left">Impact</button></li>
                </ul>
            </div>
            <div>
                <h4 className="font-bold mb-4">Company</h4>
                <ul className="space-y-2 text-sm text-gray-500">
                    <li><button className="hover:text-black text-left">About</button></li>
                    <li><button className="hover:text-black text-left">Careers</button></li>
                    <li><button className="hover:text-black text-left">Contact</button></li>
                </ul>
            </div>
        </div>
      </div>
      <div className="border-t border-gray-100 pt-8 flex flex-col md:flex-row justify-between items-center text-sm text-gray-400">
          <p>© 2025 HealthForce Goa Inc. All rights reserved.</p>
          <div className="flex gap-6 mt-4 md:mt-0">
              <a href="#" className="hover:text-black">Privacy Policy</a>
              <a href="#" className="hover:text-black">Terms of Service</a>
          </div>
      </div>
    </div>
  </footer>
);

// --- PAGES ---

const HomePage = ({ setPage }) => {
  return (
    <div className="animate-in fade-in duration-500">
      {/* HERO SECTION */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-24 pt-12">
          <div className="max-w-5xl mx-auto text-center py-16">
              <h1 className="text-5xl md:text-8xl font-extrabold tracking-tight leading-[1.1] mb-8">
                  It finds, <span className="text-green-500">predicts,</span> <br className="hidden md:block" />
                  and <span className="text-green-500">takes action.</span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-500 max-w-3xl mx-auto leading-relaxed">
                  The first Multi-Agent System for healthcare surge management. 
                  Built on LangGraph & MCP to handle the chaos so you can handle the care.
              </p>
          </div>

          <div className="relative w-full bg-[#1A4023] rounded-[2.5rem] overflow-hidden min-h-[600px] md:min-h-[700px] flex items-center justify-center shadow-2xl">
              {/* Abstract Patterns */}
              <div className="absolute inset-0 overflow-hidden">
                  <div className="absolute -top-40 -right-40 w-[600px] h-[600px] bg-green-400/20 rounded-full blur-3xl"></div>
                  <div className="absolute bottom-0 left-0 w-full h-1/2 bg-gradient-to-t from-black/40 to-transparent"></div>
              </div>

              {/* Floating UI Container */}
              <div className="relative z-10 w-full max-w-4xl px-4 md:px-0 h-full flex flex-col justify-center items-center">
                  
                  {/* Doctor Agent Alert */}
                  <div className="absolute top-12 md:top-20 left-4 md:left-12 animate-float z-20 max-w-xs w-full">
                      <div className="bg-white/90 backdrop-blur-md border border-white/50 shadow-xl rounded-2xl p-5 transform rotate-[-2deg] hover:rotate-0 transition-transform duration-300">
                          <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center gap-2">
                                  <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-orange-500">
                                      <Activity className="w-4 h-4" />
                                  </div>
                                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500">Doctor Agent</span>
                              </div>
                              <span className="flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                              </span>
                          </div>
                          <p className="text-sm font-semibold text-gray-800 leading-snug">
                              "Predicting <span className="text-red-600 font-bold">420 patients</span> in South Zone (next 48h). Severity: High."
                          </p>
                          <div className="mt-3 flex gap-2">
                              <span className="bg-gray-100 text-gray-600 text-[10px] px-2 py-1 rounded-md font-medium">Twitter Signal</span>
                              <span className="bg-gray-100 text-gray-600 text-[10px] px-2 py-1 rounded-md font-medium">ER Logs</span>
                          </div>
                      </div>
                  </div>

                  {/* Main Orchestrator Action */}
                  <div className="bg-[#141414]/90 backdrop-blur-md rounded-3xl p-6 md:p-8 w-full max-w-lg shadow-2xl border border-gray-700/50 transform transition hover:scale-[1.02] duration-500 text-white">
                      <div className="flex items-center gap-3 mb-6 pb-4 border-b border-gray-700">
                          <div className="w-3 h-3 rounded-full bg-red-500"></div>
                          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                          <div className="w-3 h-3 rounded-full bg-green-500"></div>
                          <div className="ml-auto text-xs text-gray-400 font-mono">ID: ORCH-2025-X9</div>
                      </div>
                      
                      <div className="space-y-5">
                          <div className="flex gap-4">
                              <div className="w-10 h-10 rounded-full bg-blue-600 flex-shrink-0 flex items-center justify-center text-white font-bold">Or</div>
                              <div className="space-y-1">
                                  <div className="text-xs text-gray-400">Orchestrator Agent</div>
                                  <div className="bg-gray-800 rounded-r-xl rounded-bl-xl p-4 text-sm text-gray-200 leading-relaxed">
                                      Based on DoctorAgent's forecast, we need to increase staffing and secure antibiotics. 
                                      <br/><br/>
                                      <span className="text-green-400">Recommended Action:</span> Approve overtime for +6 nurses and expedite 600 units of Paracetamol.
                                  </div>
                              </div>
                          </div>

                          <div className="pl-14 flex gap-3">
                              <button className="flex-1 bg-green-500 hover:bg-green-400 text-black font-bold py-3 px-4 rounded-xl text-sm transition-colors flex items-center justify-center gap-2 group">
                                  Approve Plan
                                  <CheckCircle2 className="w-4 h-4 group-hover:scale-110 transition-transform" />
                              </button>
                              <button className="bg-gray-700 hover:bg-gray-600 text-white font-medium py-3 px-4 rounded-xl text-sm transition-colors">
                                  Modify
                              </button>
                          </div>
                      </div>
                  </div>

                  {/* Supplier Response */}
                  <div className="absolute bottom-12 md:bottom-20 right-4 md:right-12 animate-float-delayed z-20 max-w-xs w-full">
                      <div className="bg-white/90 backdrop-blur-md border border-white/50 shadow-xl rounded-2xl p-5 transform rotate-[2deg] hover:rotate-0 transition-transform duration-300">
                          <div className="flex items-center justify-between mb-3">
                              <div className="flex items-center gap-2">
                                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600">
                                      <Truck className="w-4 h-4" />
                                  </div>
                                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500">Supplier Agent</span>
                              </div>
                              <span className="text-green-600 text-xs font-bold bg-green-100 px-2 py-0.5 rounded-full">Online</span>
                          </div>
                          <p className="text-sm text-gray-600 mb-2">Negotiating with Vendor A...</p>
                          <div className="bg-gray-50 rounded-lg p-3 border border-gray-100">
                              <div className="flex justify-between items-center text-sm">
                                  <span className="font-medium">Expedited Delivery</span>
                                  <span className="font-bold text-gray-900">24 Hours</span>
                              </div>
                              <div className="flex justify-between items-center text-xs text-gray-500 mt-1">
                                  <span>Cost Impact</span>
                                  <span className="text-red-500 font-medium">+10% Premium</span>
                              </div>
                          </div>
                      </div>
                  </div>

              </div>
          </div>
      </section>

      {/* AGENTS TEASER GRID */}
      <section className="bg-gray-50 py-24">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="mb-16 max-w-3xl">
                  <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
                      Your workforce, <br/>
                      <span className="text-gray-400">supercharged by agents.</span>
                  </h2>
                  <p className="text-lg text-gray-600">
                      HealthForce Goa isn't a chatbot. It's a team of specialized agents that work together to solve complex logistical and clinical problems in real-time.
                  </p>
                  <button onClick={() => setPage('agents')} className="mt-6 text-black font-semibold flex items-center gap-2 hover:gap-3 transition-all">
                      Explore all agents <ArrowRight className="w-4 h-4" />
                  </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {/* Doctor */}
                  <div className="bg-[#FF9F66] rounded-[2rem] p-8 min-h-[420px] flex flex-col justify-between group hover:scale-[1.02] transition-transform duration-300 shadow-lg shadow-orange-200 cursor-pointer" onClick={() => setPage('agents')}>
                      <div>
                          <div className="w-12 h-12 bg-white/30 backdrop-blur rounded-2xl flex items-center justify-center mb-6 text-white">
                              <Activity className="w-6 h-6" />
                          </div>
                          <h3 className="text-3xl font-bold mb-3 text-gray-900">Doctor<br/>Agent</h3>
                          <p className="text-gray-900/80 font-medium leading-relaxed">
                              Ingests early symptom signals and ER logs. Predicts patient counts.
                          </p>
                      </div>
                  </div>

                  {/* Pharmacy */}
                  <div className="bg-[#FDFD96] rounded-[2rem] p-8 min-h-[420px] flex flex-col justify-between group hover:scale-[1.02] transition-transform duration-300 shadow-lg shadow-yellow-100 cursor-pointer" onClick={() => setPage('agents')}>
                      <div>
                          <div className="w-12 h-12 bg-black/5 backdrop-blur rounded-2xl flex items-center justify-center mb-6 text-gray-800">
                              <Pill className="w-6 h-6" />
                          </div>
                          <h3 className="text-3xl font-bold mb-3 text-gray-900">Pharmacy<br/>Agent</h3>
                          <p className="text-gray-800/80 font-medium leading-relaxed">
                              Monitors inventory against forecasts. Triggers reorders automatically.
                          </p>
                      </div>
                  </div>

                  {/* Supplier */}
                  <div className="bg-[#A0D2EB] rounded-[2rem] p-8 min-h-[420px] flex flex-col justify-between group hover:scale-[1.02] transition-transform duration-300 shadow-lg shadow-blue-100 cursor-pointer" onClick={() => setPage('agents')}>
                      <div>
                          <div className="w-12 h-12 bg-white/30 backdrop-blur rounded-2xl flex items-center justify-center mb-6 text-blue-900">
                              <Truck className="w-6 h-6" />
                          </div>
                          <h3 className="text-3xl font-bold mb-3 text-gray-900">Supplier<br/>Agent</h3>
                          <p className="text-gray-900/80 font-medium leading-relaxed">
                              Negotiates lead times and confirms capacities via APIs.
                          </p>
                      </div>
                  </div>

                  {/* Public Health */}
                  <div className="bg-[#E0BBE4] rounded-[2rem] p-8 min-h-[420px] flex flex-col justify-between group hover:scale-[1.02] transition-transform duration-300 shadow-lg shadow-purple-200 cursor-pointer" onClick={() => setPage('agents')}>
                      <div>
                          <div className="w-12 h-12 bg-white/30 backdrop-blur rounded-2xl flex items-center justify-center mb-6 text-purple-900">
                              <Megaphone className="w-6 h-6" />
                          </div>
                          <h3 className="text-3xl font-bold mb-3 text-gray-900">Public Health<br/>Agent</h3>
                          <p className="text-gray-900/80 font-medium leading-relaxed">
                              Generates patient advisories based on confirmed surge data.
                          </p>
                      </div>
                  </div>
              </div>
          </div>
      </section>
      
      {/* ORCHESTRATION TEASER */}
      <section className="py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
         <div className="bg-black rounded-[3rem] text-white p-8 md:p-20 relative overflow-hidden flex flex-col items-center text-center">
             <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-green-500/10 rounded-full blur-[100px]"></div>
             <h2 className="text-4xl md:text-6xl font-bold mb-6 relative z-10">The Orchestrator</h2>
             <p className="text-xl text-gray-400 max-w-2xl mb-10 relative z-10">
                 Resolves conflicts between budget caps and medical needs using OR-Tools and Human-in-the-Loop gates.
             </p>
             <button onClick={() => setPage('architecture')} className="bg-white text-black px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-200 transition-colors relative z-10">
                 View System Architecture
             </button>
         </div>
      </section>
    </div>
  );
};

const AgentsPage = () => {
  const agents = [
    {
      name: "Doctor Agent",
      role: "Clinical Forecasting",
      color: "bg-[#FF9F66]",
      icon: Activity,
      inputs: ["Early symptom signals (Twitter/News)", "Local trends", "RAG Clinical SOPs", "ER Logs"],
      outputs: ["Forecasted patient counts", "Triage thresholds", "Staffing needs (+/- Doctors, Nurses)"],
      tools: ["Retriever (Vector DB)", "EHR Read API", "Orchestrator Publish"]
    },
    {
      name: "Pharmacy Agent",
      role: "Inventory & Supply",
      color: "bg-[#FDFD96]",
      icon: Pill,
      inputs: ["Forecasted prescriptions", "Current stock levels", "Historic refill rates", "Supplier ETAs"],
      outputs: ["Reorder suggestions", "Urgent demand lists", "Stockout warnings"],
      tools: ["Inventory DB", "SupplierAgent API", "Purchase API (Google AP2)"]
    },
    {
      name: "Supplier Agent",
      role: "Logistics & Negotiation",
      color: "bg-[#A0D2EB]",
      icon: Truck,
      inputs: ["Demand orders", "Capacity constraints", "Lead-times", "Shipping delays"],
      outputs: ["Confirmed order capacities", "Expedited options", "Cost estimates"],
      tools: ["Supplier DB", "Order API", "Negotiation LLM"]
    },
    {
      name: "Public Health Agent",
      role: "Advisory & Communication",
      color: "bg-[#E0BBE4]",
      icon: Megaphone,
      inputs: ["Model forecasts", "Official policy docs", "Regional restrictions", "AQI Data"],
      outputs: ["Patient advisories", "Prevention messaging", "Triage guidance"],
      tools: ["Messaging API (SMS/Email)", "Content Gen LLM", "Style Templates"]
    },
    {
      name: "Orchestrator Agent",
      role: "Central Command",
      color: "bg-black text-white",
      icon: Zap,
      inputs: ["All agent messages", "Budget constraints", "Risk thresholds"],
      outputs: ["Final prioritized action list", "Escalations to HumanSupervisor"],
      tools: ["OR-Tools Optimization", "Conflict Resolver", "Cost-Benefit Module"]
    }
  ];

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 pt-12 pb-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 bg-gray-100 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider text-gray-600 mb-4">
            <Users className="w-4 h-4" /> Multi-Agent System
          </div>
          <h1 className="text-4xl md:text-6xl font-bold mb-6">Meet the Workforce.</h1>
          <p className="text-xl text-gray-500">
            Each agent is an independent entity with specific goals, tools, and permission sets. They communicate via the <span className="text-black font-semibold">Agent-to-Agent (A2A)</span> protocol.
          </p>
        </div>

        <div className="space-y-12">
          {agents.map((agent, index) => (
            <div key={index} className={`rounded-[2.5rem] p-8 md:p-12 ${agent.color === 'bg-black text-white' ? 'bg-black text-white' : 'bg-white border border-gray-200 shadow-xl'}`}>
              <div className="flex flex-col lg:flex-row gap-12">
                <div className="lg:w-1/3">
                  <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-6 ${agent.color === 'bg-black text-white' ? 'bg-gray-800 text-white' : `${agent.color} text-black`}`}>
                    <agent.icon className="w-8 h-8" />
                  </div>
                  <h2 className="text-3xl font-bold mb-2">{agent.name}</h2>
                  <p className={`text-lg font-medium mb-6 ${agent.color === 'bg-black text-white' ? 'text-gray-400' : 'text-gray-500'}`}>{agent.role}</p>
                  <div className="flex flex-wrap gap-2">
                    {agent.tools.map((tool, i) => (
                      <span key={i} className={`text-xs px-3 py-1 rounded-full border ${agent.color === 'bg-black text-white' ? 'border-gray-700 bg-gray-900' : 'border-gray-200 bg-gray-50'}`}>
                        {tool}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="lg:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className={`p-6 rounded-2xl ${agent.color === 'bg-black text-white' ? 'bg-gray-900' : 'bg-gray-50'}`}>
                    <h3 className="font-bold mb-4 flex items-center gap-2">
                      <ArrowRight className="w-4 h-4" /> Inputs
                    </h3>
                    <ul className="space-y-3">
                      {agent.inputs.map((input, i) => (
                        <li key={i} className="text-sm opacity-80 border-l-2 border-current pl-3">
                          {input}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div className={`p-6 rounded-2xl ${agent.color === 'bg-black text-white' ? 'bg-gray-900' : 'bg-gray-50'}`}>
                    <h3 className="font-bold mb-4 flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4" /> Outputs
                    </h3>
                    <ul className="space-y-3">
                      {agent.outputs.map((output, i) => (
                        <li key={i} className="text-sm opacity-80 border-l-2 border-current pl-3">
                          {output}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const ArchitecturePage = () => {
  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 pt-12 pb-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">System Architecture</h1>
          <p className="text-xl text-gray-500">
            A modular, containerized stack designed for real-world deployability using Google Cloud Platform, LangGraph, and MCP.
          </p>
        </div>

        {/* Tech Stack Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-20">
            {[
              { name: "LangGraph", desc: "Agent Orchestration", icon: Share2 },
              { name: "MCP", desc: "Context Protocol", icon: Database },
              { name: "Google AP2", desc: "Agent Payments", icon: Zap },
              { name: "PostgreSQL", desc: "Structured Data", icon: Server },
              { name: "FastAPI", desc: "Backend API", icon: Cpu },
              { name: "React", desc: "Frontend Dashboard", icon: Activity },
              { name: "Docker", desc: "Containerization", icon: Server },
              { name: "Chroma", desc: "Vector Search", icon: Database },
            ].map((tech, i) => (
              <div key={i} className="bg-white border border-gray-200 p-6 rounded-xl flex flex-col items-center text-center hover:shadow-lg transition-shadow">
                <tech.icon className="w-8 h-8 mb-4 text-gray-800" />
                <h3 className="font-bold text-lg">{tech.name}</h3>
                <p className="text-sm text-gray-500">{tech.desc}</p>
              </div>
            ))}
        </div>

        {/* Logic Flow Diagram Visualization */}
        <div className="bg-[#0f172a] text-white rounded-3xl p-8 md:p-12 shadow-2xl overflow-hidden relative">
           <div className="absolute top-0 right-0 p-4 text-xs font-mono text-gray-500">FLOW: SURGE_RESPONSE</div>
           
           <div className="relative z-10 flex flex-col items-center gap-8">
              {/* Step 1 */}
              <div className="w-full max-w-2xl bg-gray-800/50 border border-gray-700 p-4 rounded-xl flex items-center gap-4">
                <div className="bg-orange-500/20 p-2 rounded-lg"><Activity className="text-orange-500" /></div>
                <div>
                  <div className="font-bold text-sm text-orange-400">Step 1: Ingestion</div>
                  <div className="text-xs text-gray-300">Scrapers (Twitter/Reddit) + ER Logs &rarr; Vector DB (Chroma)</div>
                </div>
              </div>
              <div className="h-8 w-0.5 bg-gray-700"></div>

              {/* Step 2 */}
              <div className="w-full max-w-2xl bg-gray-800/50 border border-gray-700 p-4 rounded-xl flex items-center gap-4">
                <div className="bg-blue-500/20 p-2 rounded-lg"><Cpu className="text-blue-500" /></div>
                <div>
                  <div className="font-bold text-sm text-blue-400">Step 2: Prediction</div>
                  <div className="text-xs text-gray-300">DoctorAgent uses RAG to forecast patient surge & severity breakdown.</div>
                </div>
              </div>
              <div className="h-8 w-0.5 bg-gray-700"></div>

              {/* Step 3 */}
              <div className="w-full max-w-2xl bg-gray-800/50 border border-gray-700 p-4 rounded-xl flex items-center gap-4">
                <div className="bg-yellow-500/20 p-2 rounded-lg"><Zap className="text-yellow-500" /></div>
                <div>
                  <div className="font-bold text-sm text-yellow-400">Step 3: Optimization</div>
                  <div className="text-xs text-gray-300">Orchestrator runs <code>min(cost + wait_time)</code> subject to budget constraints.</div>
                </div>
              </div>
              <div className="h-8 w-0.5 bg-gray-700"></div>

              {/* Step 4 */}
              <div className="w-full max-w-2xl bg-gray-800/50 border border-green-500/50 p-4 rounded-xl flex items-center gap-4 shadow-[0_0_20px_rgba(34,197,94,0.2)]">
                <div className="bg-green-500/20 p-2 rounded-lg"><CheckCircle2 className="text-green-500" /></div>
                <div>
                  <div className="font-bold text-sm text-green-400">Step 4: Execution</div>
                  <div className="text-xs text-gray-300">Staff Scheduling + Medicine Reorder (Payment via Google AP2) + Public Alert.</div>
                </div>
              </div>
           </div>
        </div>

        <div className="mt-16 bg-gray-50 border border-gray-200 p-8 rounded-2xl">
          <h3 className="font-bold text-xl mb-4">Deployment</h3>
          <p className="text-gray-600 mb-4">
            The system is containerized with Docker. Each agent runs as a separate service communicating via Redis Streams, ensuring scalability and fault tolerance.
          </p>
          <code className="block bg-gray-900 text-green-400 p-4 rounded-lg text-sm font-mono overflow-x-auto">
            docker-compose up --scale doctor-agent=3 --scale orchestrator=1
          </code>
        </div>
      </div>
    </div>
  );
};

const ImpactPage = () => {
  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 pt-12 pb-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row gap-16 items-center mb-24">
          <div className="md:w-1/2">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">Why we built this.</h1>
            <p className="text-xl text-gray-500 mb-8 leading-relaxed">
              Hospitals are currently reactive. By the time they mobilize for a pollution wave or viral outbreak, critical delays have already occurred. 
              <br/><br/>
              HealthForce Goa shifts healthcare from <span className="text-red-500 font-bold">Reactive</span> to <span className="text-green-600 font-bold">Predictive</span>.
            </p>
          </div>
          <div className="md:w-1/2">
             <div className="grid grid-cols-2 gap-4">
                <div className="bg-red-50 p-6 rounded-2xl border border-red-100">
                  <div className="text-red-500 font-bold mb-2">Before</div>
                  <ul className="text-sm space-y-2 text-red-800">
                    <li>• Stockouts during panic</li>
                    <li>• Understaffed ERs</li>
                    <li>• Delayed public warnings</li>
                    <li>• High wastage of deadstock</li>
                  </ul>
                </div>
                <div className="bg-green-50 p-6 rounded-2xl border border-green-100">
                  <div className="text-green-600 font-bold mb-2">After (Avyott)</div>
                  <ul className="text-sm space-y-2 text-green-800">
                    <li>• Pre-stocked essentials</li>
                    <li>• Optimized shift rosters</li>
                    <li>• Instant localized alerts</li>
                    <li>• Data-driven procurement</li>
                  </ul>
                </div>
             </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-3xl shadow-lg border border-gray-100">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 mb-6">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Predictive Preparedness</h3>
            <p className="text-gray-600">
              Reduces chaos during epidemics by ensuring hospitals are stocked and staffed days in advance.
            </p>
          </div>

          <div className="bg-white p-8 rounded-3xl shadow-lg border border-gray-100">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600 mb-6">
              <Zap className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Cost Efficiency</h3>
            <p className="text-gray-600">
              Minimizes wastage of drugs and expensive emergency procurement through intelligent forecasting.
            </p>
          </div>

          <div className="bg-white p-8 rounded-3xl shadow-lg border border-gray-100">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mb-6">
              <HeartPulse className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-bold mb-4">Public Safety</h3>
            <p className="text-gray-600">
              Directly saves lives by sending real-time advisory messages to citizens in high-risk zones.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const DemoPage = () => {
  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 pt-12 pb-24">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-12 border border-gray-100">
          <div className="text-center mb-10">
            <h1 className="text-3xl md:text-5xl font-bold mb-4">Book a Demo</h1>
            <p className="text-gray-500">
              See the Multi-Agent System in action. We'll simulate a patient surge using real historical data.
            </p>
          </div>

          <form className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">First Name</label>
                <input type="text" className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black" placeholder="Jane" />
              </div>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">Last Name</label>
                <input type="text" className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black" placeholder="Doe" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Work Email</label>
              <input type="email" className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black" placeholder="jane@hospital.com" />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Organization Type</label>
              <select className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black">
                <option>Hospital Chain</option>
                <option>Local Clinic</option>
                <option>Government Health Dept</option>
                <option>Pharmaceutical Supplier</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Interest Area</label>
              <div className="flex flex-wrap gap-3">
                {['Staff Optimization', 'Inventory Prediction', 'Public Health Alerts', 'Full Platform'].map((tag) => (
                  <label key={tag} className="inline-flex items-center gap-2 cursor-pointer bg-gray-50 px-4 py-2 rounded-full border border-gray-200 hover:border-black transition-colors">
                    <input type="checkbox" className="w-4 h-4 text-black rounded" />
                    <span className="text-sm">{tag}</span>
                  </label>
                ))}
              </div>
            </div>

            <button type="button" className="w-full bg-black text-white font-bold text-lg py-4 rounded-xl hover:bg-gray-800 transition-transform active:scale-[0.98]">
              Schedule Simulation
            </button>
          </form>

          <div className="mt-8 pt-8 border-t border-gray-100 flex justify-center gap-8 text-gray-400">
             <div className="flex items-center gap-2">
               <ShieldCheck className="w-4 h-4" /> SOC2 Compliant
             </div>
             <div className="flex items-center gap-2">
               <Server className="w-4 h-4" /> HIPAA Ready
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const LoginPage = ({ setPage }) => {
  const [activeTab, setActiveTab] = useState('hospital');

  const roles = [
    { 
      id: 'hospital', 
      label: 'Hospital', 
      icon: Activity, 
      description: 'View staffing forecasts & orchestrate resources.',
      alertMessage: 'CRITICAL: Predicted surge of +420 patients in next 48h. Staffing shortage detected.',
      alertColor: 'bg-red-50 border-red-100 text-red-800'
    },
    { 
      id: 'pharmacy', 
      label: 'Pharmacy', 
      icon: Pill, 
      description: 'Track inventory & approve automated restocks.',
      alertMessage: 'WARNING: Paracetamol stock below safety buffer (15%). Auto-reorder pending approval.',
      alertColor: 'bg-yellow-50 border-yellow-100 text-yellow-800'
    },
    { 
      id: 'patient', 
      label: 'Patient', 
      icon: HeartPulse, 
      description: 'Receive real-time health advisories & triage.',
      alertMessage: 'ADVISORY: Air Quality Index is "Severe" (450+). Respiratory cases rising. Wear a mask.',
      alertColor: 'bg-purple-50 border-purple-100 text-purple-800'
    },
  ];

  const currentRole = roles.find(r => r.id === activeTab);

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 pt-12 pb-24 min-h-screen flex items-center justify-center bg-gray-50/50">
      <div className="w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row gap-8 items-stretch">
        
        {/* Left Side - Context */}
        <div className="md:w-5/12 bg-black text-white rounded-3xl p-10 flex flex-col justify-between relative overflow-hidden shadow-2xl">
           <div className="absolute top-0 right-0 w-[300px] h-[300px] bg-green-500/20 rounded-full blur-[80px]"></div>
           
           <div className="relative z-10">
             <div className="w-12 h-12 bg-white/10 backdrop-blur rounded-xl flex items-center justify-center mb-8">
               <ShieldCheck className="w-6 h-6 text-green-400" />
             </div>
             <h2 className="text-3xl font-bold mb-4">Secure Access</h2>
             <p className="text-gray-400 text-lg leading-relaxed mb-6">
               Log in to your specific role node to view real-time alerts, manage resources, and coordinate with the mesh network.
             </p>
             
             {/* Dynamic Role Context in Left Panel */}
             <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/10">
                <div className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Current Role Context</div>
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-black/40 rounded-lg">
                        <currentRole.icon className="w-5 h-5 text-white" />
                    </div>
                    <div className="text-sm font-medium">{currentRole.description}</div>
                </div>
             </div>
           </div>

           <div className="relative z-10 mt-12 space-y-4">
              <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800 flex items-center gap-4">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <div className="text-sm">
                  <span className="text-gray-400">System Status:</span> <span className="text-white font-bold">Operational</span>
                </div>
              </div>
              <div className="bg-gray-900/50 p-4 rounded-xl border border-gray-800 flex items-center gap-4">
                 <Server className="w-4 h-4 text-blue-400" />
                 <div className="text-sm text-gray-400">
                   Secure connection via <span className="text-white font-mono">MCP Protocol</span>
                 </div>
              </div>
           </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="md:w-7/12 bg-white rounded-3xl shadow-xl border border-gray-100 p-8 md:p-12 relative overflow-hidden">
           <div className="mb-8">
             <h3 className="text-2xl font-bold mb-2">Welcome back.</h3>
             <p className="text-gray-500">Choose your role to continue.</p>
           </div>

           {/* Role Tabs */}
           <div className="grid grid-cols-3 gap-2 mb-8 bg-gray-100 p-1 rounded-xl">
              {roles.map((role) => (
                <button
                  key={role.id}
                  onClick={() => setActiveTab(role.id)}
                  className={`flex flex-col items-center justify-center py-3 px-2 rounded-lg text-sm font-medium transition-all ${activeTab === role.id ? 'bg-white shadow-sm text-black scale-[1.02]' : 'text-gray-500 hover:text-gray-700'}`}
                >
                  <role.icon className={`w-5 h-5 mb-1 ${activeTab === role.id ? 'text-green-600' : 'text-gray-400'}`} />
                  {role.label}
                </button>
              ))}
           </div>

           {/* ACTIVE ALERT BOX - DYNAMIC */}
           <div className={`border rounded-xl p-4 mb-8 flex items-start gap-3 transition-colors duration-300 ${currentRole.alertColor}`}>
              <div className="mt-1 flex-shrink-0">
                  <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                  <div className="text-xs font-bold uppercase tracking-wider opacity-80 mb-1">Active Alert</div>
                  <p className="text-sm font-semibold leading-snug">
                    {currentRole.alertMessage}
                  </p>
              </div>
           </div>

           {/* Form */}
           <form className="space-y-5" onSubmit={(e) => { e.preventDefault(); alert(`Logging in as ${activeTab}...`); }}>
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  {activeTab === 'patient' ? 'Mobile Number / Health ID' : 'Employee ID / Email'}
                </label>
                <input type="text" className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black transition-shadow" placeholder={activeTab === 'patient' ? '+91 98765 43210' : 'admin@healthforce.goa'} />
              </div>
              
              <div>
                 <div className="flex justify-between mb-2">
                    <label className="block text-sm font-bold text-gray-700">Password</label>
                    <a href="#" className="text-xs text-gray-400 hover:text-black">Forgot?</a>
                 </div>
                 <input type="password" className="w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-black transition-shadow" placeholder="••••••••" />
              </div>

              <button className="w-full bg-black text-white font-bold text-lg py-4 rounded-xl hover:bg-gray-800 transition-transform active:scale-[0.99] flex items-center justify-center gap-2">
                Access Dashboard <ArrowRight className="w-5 h-5" />
              </button>
           </form>
        </div>

      </div>
    </div>
  );
};

// --- MAIN APP ---

const App = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'home': return <HomePage setPage={setCurrentPage} />;
      case 'agents': return <AgentsPage />;
      case 'architecture': return <ArchitecturePage />;
      case 'impact': return <ImpactPage />;
      case 'demo': return <DemoPage />;
      case 'login': return <LoginPage setPage={setCurrentPage} />;
      default: return <HomePage setPage={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans selection:bg-green-100 selection:text-green-900">
      <GlobalStyles />
      <Navbar currentPage={currentPage} setPage={setCurrentPage} isScrolled={isScrolled} />
      <main className="pt-20 min-h-screen">
        {renderPage()}
      </main>
      <Footer setPage={setCurrentPage} />
    </div>
  );
};

export default App;