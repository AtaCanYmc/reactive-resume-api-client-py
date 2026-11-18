class Rxresume < Formula
  include Language::Python::Virtualenv

  desc "Reactive Resume API client, CLI, and FastMCP server"
  homepage "https://github.com/AtaCanYmc/reactive-resume-api-client-py"
  url "https://github.com/AtaCanYmc/reactive-resume-api-client-py/archive/refs/tags/v0.6.0.tar.gz" # x-release-please-version
  sha256 "0dde9f0dbcdd0488fb5059eea3276bfeea1bae206864cb9bd07bb7884f40db8c"
  license "MIT"
  head "https://github.com/AtaCanYmc/reactive-resume-api-client-py.git", branch: "main"

  depends_on "certifi"
  depends_on "pydantic"
  depends_on "python@3.14"

  resource "anyio" do
    url "https://files.pythonhosted.org/packages/a1/98/7e457a3b014976887a050561955c0b76e1e7e2d6e27b78ecef2ef80518f2/anyio-4.16.0.tar.gz"
    sha256 "59bb03251907983d1603d27c3087ddb1e93299ea2163adcdba37899a4fb12ffb"
  end

  resource "dnspython" do
    url "https://files.pythonhosted.org/packages/1e/0c/5346358b3a20275d256978c35203ddc2c8617f78c1b23795b79ba22ced6d/dnspython-2.9.2-py3-none-any.whl"
    sha256 "af15f7d385a6ae2fb35a796fde2138004c8c42c7389090e2addc83e3b3340fd8"
  end

  resource "email-validator" do
    url "https://files.pythonhosted.org/packages/c0/4d/f5e9d9de19f4b8f9e33d802fe3efb0ef96e88d4d6d45d604f335bef2f1ef/email_validator-2.4.0.tar.gz"
    sha256 "be487bc50bc3bd832a98515a55a15649d9bec06d954fa178663190714b6c4ee1"
  end

  resource "h11" do
    url "https://files.pythonhosted.org/packages/01/ee/02a2c011bdab74c6fb3c75474d40b3052059d95df7e73351460c8588d963/h11-0.16.0.tar.gz"
    sha256 "4e35b956cf45792e4caa5885e69fba00bdbc6ffafbfa020300e549b208ee5ff1"
  end

  resource "httpcore" do
    url "https://files.pythonhosted.org/packages/06/94/82699a10bca87a5556c9c59b5963f2d039dbd239f25bc2a63907a05a14cb/httpcore-1.0.9.tar.gz"
    sha256 "6e34463af53fd2ab5d807f399a9b45ea31c3dfa2276f15a2c3f00afff6e176e8"
  end

  resource "httpx" do
    url "https://files.pythonhosted.org/packages/b1/df/48c586a5fe32a0f01324ee087459e112ebb7224f646c0b5023f5e79e9956/httpx-0.28.1.tar.gz"
    sha256 "75e98c5f16b0f35b567856f597f06ff2270a374470a5c2392242528e3e3e42fc"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/f5/08/8eea9d4b8302028f3abb2c0813953f7aec26d33b7a8960ed760e65ff29fa/idna-3.20.tar.gz"
    sha256 "a7db850025b95ded1eae8a46181a1a6c56c92c96f0e2b005d9ff8dc0210cab44"
  end

  resource "typing-extensions" do
    url "https://files.pythonhosted.org/packages/f6/cc/6253133b5bb138fc3306cebfbda2c520f545d36b5be2c7255cc528bb45d6/typing_extensions-4.16.0.tar.gz"
    sha256 "dc983d19a509c94dba722ee6abd33940f7c05a89e243c47e907eb4db6f1a43e5"
  end

  def install
    venv = virtualenv_create(libexec, "python3.14", system_site_packages: true)
    venv.pip_install resources
    venv.pip_install_and_link buildpath
  end

  test do
    assert_match "rxresume", shell_output("#{bin}/rxresume --help")
  end
end
